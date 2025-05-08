import gazu
import os

#kitsu_url = os.getenv("KITSU_URL")
#kitsu_email = os.getenv("KITSU_EMAIL")
#kitsu_password = os.getenv("KITSU_PASSWORD")

# FIXME: This should take the info from the GUI and set as env variables
def set_env_variables(kitsu_url, kitsu_email, kitsu_password):
    #os.environ["KITSU_URL"] = kitsu_url
    #os.environ["KITSU_EMAIL"] = kitsu_email
    #os.environ["KITSU_PASSWORD"] = kitsu_password
    print("Setting environment variables")
    print(f"KITSU_URL: {kitsu_url}")
    print(f"KITSU_EMAIL: {kitsu_email}")
    print(f"KITSU_PASSWORD: {kitsu_password}")


#if kitsu_url and kitsu_url.startswith("https://"):
#    print("Warning your KITSU_URL is using https instead of http")
# Login
def connect_to_kitsu(kitsu_url, kitsu_email, kitsu_password):
    gazu.client.set_host(kitsu_url)
    logged_in = gazu.log_in(kitsu_email, kitsu_password)
    if logged_in:
        print("Kitsu Login successful!")
    else:
        print("Login failed.")


#connect_to_kitsu()