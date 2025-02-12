import re
from math import ceil
from .data_fetcher import fetch_data
from .data_fetcher import get_page_source
from .data_processor import get_experience_data, get_experience_datas
import urllib.parse

def getLikersList(post_url, current_timestamp):

    response = get_page_source(post_url)

    html_content = response.text
    pattern = r"urn:li:ugcPost:(\d+)" 
    post_id = re.findall(pattern, html_content)[0]

    url = f'https://www.linkedin.com/voyager/api/graphql?includeWebMetadata=true&variables=(count:10,start:0,threadUrn:urn%3Ali%3AugcPost%3A{post_id})&queryId=voyagerSocialDashReactions.cab051ffdf47c41130cdd414e0097402'

    data = fetch_data(url)

    if data:

        total = data["data"]["data"]["socialDashReactionsByReactionType"]["paging"]["total"]

        print('Total Likers: ', total)

        request_num = ceil(total/100)
        likers_info = []
        actoUrns = []
        element_number = 1

        for i in range(request_num):

            url = f'https://www.linkedin.com/voyager/api/graphql?includeWebMetadata=true&variables=(count:100,start:{i * 100},threadUrn:urn%3Ali%3AugcPost%3A7290004779827703810)&queryId=voyagerSocialDashReactions.cab051ffdf47c41130cdd414e0097402'
            response = fetch_data(url)

            if response:
                
                data = response
                for element in data['included']:
                    full_name = None
                    connection_degree = None
                    root_url = None
                    artifacts = None
                    profile_url = None

                    if element and element.get("actorUrn"):

                        actoUrns.append(element.get("actorUrn"))

                        if element.get("reactorLockup"):

                            full_name = element["reactorLockup"]["title"]["text"]
                            profile_url = element["reactorLockup"]["navigationUrl"]

                            if element.get("reactorLockup") and element["reactorLockup"].get("label"):
                                connection_degree = element["reactorLockup"]["label"]["text"]

                            if (element.get("reactorLockup") and
                                element["reactorLockup"].get("image") and
                                element["reactorLockup"]["image"].get("attributes") and
                                len(element["reactorLockup"]["image"]["attributes"]) > 0 and
                                element["reactorLockup"]["image"]["attributes"][0].get("detailData") and
                                element["reactorLockup"]["image"]["attributes"][0]["detailData"].get("nonEntityProfilePicture") and
                                element["reactorLockup"]["image"]["attributes"][0]["detailData"]["nonEntityProfilePicture"].get("vectorImage")):
                
                                root_url = element["reactorLockup"]["image"]["attributes"][0]["detailData"]["nonEntityProfilePicture"]["vectorImage"]["rootUrl"]
                                artifacts = element["reactorLockup"]["image"]["attributes"][0]["detailData"]["nonEntityProfilePicture"]["vectorImage"]["artifacts"][-1]["fileIdentifyingUrlPathSegment"]
                                avatar_url = f"{root_url}{artifacts}"

                            likers_data = {
                                "fullName": full_name,
                                "jobTitle": element.get("actorUrn"),
                                "profileUrl": profile_url,
                                "imageUrl": avatar_url,
                                "connectionDegree": connection_degree,
                                "timestamp": current_timestamp,
                            }

                            likers_info.append(likers_data)

        experience_datas = get_experience_datas(actoUrns, total)

        i = 0
        for element in likers_info:
            job_title = urllib.parse.quote(element['jobTitle'])  # Extract first
            element_url = f'https://www.linkedin.com/voyager/api/graphql?variables=(profileUrn:{job_title},sectionType:experience,locale:en_US)&queryId=voyagerIdentityDashProfileComponents.a62d9c6739ad5a19fdf61591073dec32'
 
            experience_data = next((p for p in experience_datas if p['profileUrl'] == element_url), None)
            
            if experience_data:
                likers_info[i]["jobTitle"] = experience_data['jobTitle']
                likers_info[i]["positionTitle"] = experience_data['jobTitle']
                likers_info[i]["companyLogo"] = experience_data['companyLogo']
                likers_info[i]["companyName"] = experience_data['companyName']
                likers_info[i]["locationName"] = experience_data['location']
            else: likers_info[i]["jobTitle"] = ''
            i += 1

        return likers_info
    
    else:
        print(f"Failed to retrieve likers data")
        return {}

