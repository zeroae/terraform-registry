from chalice import Chalice

from chalicelib.modules import bp as modules_bp

app = Chalice(app_name="terraform-registry")
app.experimental_feature_flags.update(["BLUEPRINTS"])
app.register_blueprint(modules_bp, url_prefix="/v1")


@app.route("/.well-known/terraform.json")
def discovery():
    """The Terraform Registry Service Discovery Protocol

       ref: https://www.terraform.io/docs/internals/remote-service-discovery.html#discovery-process
    """
    host = app.current_request.headers["host"]
    # Only HTTPS is allowed for Terraform Registry protocol
    # Use ngrok to redirect https traffic for free during development
    return {"modules.v1": f"https://{host}/v1"}
