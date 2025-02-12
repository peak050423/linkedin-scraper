from .data_fetcher import fetch_data, fetch_multiple_data
import urllib.parse
import json

def extract_experience_details(entry, experience_data):
    entity = entry.get("components", {}).get("entityComponent", {})
    company_name = None
    job_title = None
    location = None
    company_logo_urn = None
    root_url = None
    image_path = None

    if entity:
        if entity.get('subtitle') and entity['subtitle'].get('text'):
            company_name = entity.get("subtitle", {}).get("text", "").split(" \u00b7 ")[0]
        if entity.get('titleV2') and entity['titleV2'].get('text'):
            job_title = entity.get("titleV2", {}).get("text", {}).get("text", "")
        if entity.get('metadata') and entity['metadata'].get('text'):
            location = entity.get("metadata", {}).get("text", "").split(" \u00b7 ")[0]

        if entity.get("image"):
            company_logo_urn = entity.get("image", {}).get("attributes", [{}])[0].get("detailData", {}).get("*companyLogo")

        if company_logo_urn:
            for element in experience_data.get("included", []):
                if element.get("entityUrn") == company_logo_urn:
                    logo_resolution_result = element.get("logoResolutionResult")
                    if logo_resolution_result:
                        vector_image = logo_resolution_result.get("vectorImage", {})
                        if vector_image:
                            root_url = vector_image.get("rootUrl")
                            image_path = vector_image.get("artifacts", [{}])[-1].get("fileIdentifyingUrlPathSegment")
                            break

    return {
        "companyName": company_name,
        "jobTitle": job_title,
        "location": location,
        "companyLogo": f"{root_url}{image_path}" if root_url and image_path else None
    }

def get_experience_data(profile_urn, element_number, follower_number):
    encoded_profile_urn = urllib.parse.quote(profile_urn)
    profile_url = f'https://www.linkedin.com/voyager/api/graphql?variables=(profileUrn:{encoded_profile_urn},sectionType:experience,locale:en_US)&queryId=voyagerIdentityDashProfileComponents.a62d9c6739ad5a19fdf61591073dec32'

    experience_data = fetch_data(profile_url)

    if experience_data:
        records = []

        if experience_data.get("included"):
            for entry in experience_data.get("included", [])[0].get("components", {}).get("elements", []):
                record = extract_experience_details(entry, experience_data)
                records.append(record)
                break  # Only process the first entry

        return records
    else:
        print(f"Failed to retrieve experience data for {profile_urn}")
        return {}

def get_experience_datas(profile_urns, follower_number):
    profile_urls = [f'https://www.linkedin.com/voyager/api/graphql?variables=(profileUrn:{urllib.parse.quote(profile_urn)},sectionType:experience,locale:en_US)&queryId=voyagerIdentityDashProfileComponents.a62d9c6739ad5a19fdf61591073dec32' for profile_urn in profile_urns]

    experience_datas = fetch_multiple_data(profile_urls, follower_number)

    if experience_datas:
        records = []

        for url, experience_data in experience_datas.items():

            if experience_data.get("included"):
                for entry in experience_data.get("included", [])[0].get("components", {}).get("elements", []):
                    record = extract_experience_details(entry, experience_data)
                    record["profileUrl"] = url
                    records.append(record)

        return records
    else:
        print(f"Failed to retrieve experience data for the provided profile URNs")
        return {}