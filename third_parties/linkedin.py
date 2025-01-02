import os
import requests
from dotenv import load_dotenv


load_dotenv()

def scrape_linkedin_profile(linkedin_profile_url:str, mock: bool = False) -> str:
    if mock:
        linkedin_profile_url  = "https://gist.githubusercontent.com/smoneyan/1139d8d093d30739c4e54c23da6473da/raw/0317a54c8c2f183ae01297c98c69617d37ac1bc0/my-linkedin-profile.json"
        response = requests.get(
            linkedin_profile_url,
            timeout=10,
        )
    else:
        response = requests.get(
            "https://nubela.co/proxycurl/api/v2/linkedin",
            headers={
                "Authorization": f'Bearer {os.environ.get("PROXYCURL_API_KEY")}' \
            },
            params  = {
                "url": linkedin_profile_url
            },
            timeout=10,
        )

    data = response.json()
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None)
        and k not in ["people_also_viewed", "certifications", "similarly_named_profiles"]
    }
    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")
    return data


if __name__ == "__main__":
    print(
        scrape_linkedin_profile(
             linkedin_profile_url= "https://www.linkedin.com/in/s-subramanian/",
             mock=True
        )
    )
