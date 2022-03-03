from saml2.client import Saml2Client
from saml2.config import Config as Saml2Config
from saml2 import BINDING_HTTP_POST
from saml2 import BINDING_HTTP_REDIRECT
from saml2.saml import NameID
from saml2.saml import NAMEID_FORMAT_TRANSIENT
from flask import Blueprint, request, redirect, current_app, url_for
from flask_login import login_user, login_required, logout_user, current_user
from app.models.user import User
from app.models.user import Role
from app.models.config import db
from saml2.time_util import in_a_while
import os 
import requests

ENTITY_ID = "https://ramp.smart.sum.ba/saml/metadata.xml"
METADATA_URL = "https://aai.sum.ba/sso/saml2/idp/metadata.php"
ACS_URL = "https://ramp.smart.sum.ba/saml/acs/"
SLO_URL = "https://ramp.smart.sum.ba/saml/sls/"
PATH = os.path.dirname(os.path.realpath(__file__))

rv = open(PATH+"/metadata/eduid.xml").read()
auth = Blueprint('auth', __name__)

def sso_client():
    settings = {
        'entityid': ENTITY_ID,
        'metadata': {
            'inline': [rv],
        },
        'service': {
            'sp': {
                'endpoints': {
                    'assertion_consumer_service': [
                        (ACS_URL, BINDING_HTTP_POST)
                    ],
                    "single_logout_service": [
                        (SLO_URL, BINDING_HTTP_POST)
                    ],
                },
                'allow_unsolicited': True,
                'authn_requests_signed': False,
                'logout_requests_signed': False,
                'want_assertions_signed': True,
                'want_response_signed': True,
                'want_authn_requests_signed': False,
                'want_authn_requests_only_with_valid_cert': False
            }
        },
        'accepted_time_diff': 90,
        "key_file": PATH + "/keys/sp_private_key.pem",
        "cert_file": PATH + "/keys/sp_certificate.pem"
    }
    config = Saml2Config()
    config.load(settings)
    config.allow_unknown_attributes = True
    return Saml2Client(config=config)

saml_client = sso_client()

@auth.route("/saml/acs/", methods=['POST'])
def saml_acs():
    global saml_client
    authn_response = saml_client.parse_authn_request_response(
        request.form['SAMLResponse'],
        BINDING_HTTP_POST
    )
    identity = authn_response.get_identity()
    user = User.query.filter_by(eduid=identity['uid'][0]).first()
    if user == None:
        if identity["sumEduPersonRole"][0] == "administrator imenika":
            user = User()
            user.firstname = identity["givenName"][0]
            user.lastname = identity["sn"][0]
            user.eduid = identity["uid"][0]
            user.email = identity["mail"][0]
            user.role = Role.admin
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for("user.users"))
        elif identity["sumEduPersonRole"][0] == "nastavnik" or identity["sumEduPersonRole"] == "iss koordinator":
            user = User()
            user.firstname = identity["givenName"][0]
            user.lastname = identity["sn"][0]
            user.eduid = identity["uid"][0]
            user.email = identity["mail"][0]
            user.role = Role.other
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for("user.users"))
        else:
            message = {
                "error" : "Nemate pristup ovom dijelu sustava.",
                "code" : 401
            }
            return message
    else:
        login_user(user)
        return redirect(url_for("user.users"))


@auth.route("/saml/login")
def saml_login():
    global saml_client
    reqid, info = saml_client.prepare_for_authenticate(binding=BINDING_HTTP_POST)
    return info["data"]

@auth.route("/saml/sls/", methods=["GET","POST"])
def logout():
    if request.method == 'GET':
        return redirect(url_for("index"))
    else:
        global saml_client
        name_id = NameID(text=current_user.email, format=NAMEID_FORMAT_TRANSIENT)
        expected_binding = BINDING_HTTP_POST
        entity_ids = ["https://aai.sum.ba/sso/saml2/idp/metadata.php"]
        time = in_a_while(minutes=5)
        sign=False
        reason = "Tired"

        resp = saml_client.do_logout(
            name_id,
            entity_ids,
            reason,
            time,
            sign=sign,
            expected_binding=expected_binding
        )
        logout_user()
        return resp["https://aai.sum.ba/sso/saml2/idp/metadata.php"][1]["data"]