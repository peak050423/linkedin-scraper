from .data_processor import get_experience_data, get_experience_datas
from .data_fetcher import fetch_data
import urllib.parse

# Load cookies from your linkedin_cookies.json (adjust path if necessary)
def getFollowerList(company_id, follower_number, current_timestamp):
    url = f"https://www.linkedin.com/voyager/api/graphql?variables=(start:0,count:{follower_number},organizationalPage:urn%3Ali%3Afsd_organizationalPage%3A{company_id},followerType:MEMBER)&queryId=voyagerOrganizationDashFollowers.3ff930c92333c8fd237f011719ee1428"

    data = fetch_data(url)

    if data:

        followers_info = []
        element_number = 1
        member_urns = []

        for element in data['data']['data']['organizationDashFollowersByOrganizationalPage']['elements']:
            profile_urn = element['followerV2']['*profile']

            # Extract followed_at text (human-readable format)
            followed_at = element['followedAt']['text']

            # Find the corresponding profile in 'included'
            for profile in data['included']:
                if profile['entityUrn'] == profile_urn:
                    avatar_url = None
                    if 'profilePicture' in profile and profile['profilePicture']:
                        img_data = profile['profilePicture'].get('displayImageReferenceResolutionResult')
                        if img_data and 'vectorImage' in img_data:
                            root_url = img_data['vectorImage']['rootUrl']
                            artifacts = img_data['vectorImage']['artifacts']
                            if artifacts:
                                largest_artifact = artifacts[-1]
                                avatar_url = f"{root_url}{largest_artifact['fileIdentifyingUrlPathSegment']}"

                    # Extract connection degree from "memberRelationship"
                    connection_degree = 1
                    member_relationship_urn = f"{profile_urn}"
                    member_urns.append(member_relationship_urn)
                    for relationship in data['included']:
                        if 'memberRelationship' in relationship:
                            if relationship.get('entityUrn').split(":")[-1] == member_relationship_urn.split(":")[-1]:
                                connection_info = relationship.get('memberRelationship')
                                noConnection = connection_info.get('noConnection')

                                if noConnection is None:
                                    connection_degree = 1

                                else:
                                    member_distance = noConnection.get('memberDistance')

                                    # Convert member_distance to a numeric value
                                    if member_distance == "DISTANCE_1":
                                        connection_degree = 1
                                    elif member_distance == "DISTANCE_2":
                                        connection_degree = 2
                                    elif member_distance == "DISTANCE_3":
                                        connection_degree = 3
                                    elif member_distance == "OUT_OF_NETWORK":
                                        connection_degree = None
                                

                    # Prepare final follower data
                    first_name = profile.get('firstName', '')
                    last_name = profile.get('lastName', '')
                    follower_data = {
                        "fullName": first_name + ' ' + last_name,
                        # "headline": profile.get('headline', ''),
                        "jobTitle": member_relationship_urn,
                        "profileUrl": f"https://www.linkedin.com/in/{profile.get('publicIdentifier')}",
                        "imageUrl": avatar_url,
                        "connectionDegree": connection_degree,
                        "timestamp": current_timestamp,
                        "followedAt": followed_at,
                    }
                    followers_info.append(follower_data)

        experience_datas = get_experience_datas(member_urns, follower_number)

        i = 0
        for element in followers_info:
            job_title = urllib.parse.quote(element['jobTitle'])  # Extract first
            element_url = f'https://www.linkedin.com/voyager/api/graphql?variables=(profileUrn:{job_title},sectionType:experience,locale:en_US)&queryId=voyagerIdentityDashProfileComponents.a62d9c6739ad5a19fdf61591073dec32'
 
            experience_data = next((p for p in experience_datas if p['profileUrl'] == element_url), None)
            
            if experience_data:
                followers_info[i]["jobTitle"] = experience_data['jobTitle']
                followers_info[i]["positionTitle"] = experience_data['jobTitle']
                followers_info[i]["companyLogo"] = experience_data['companyLogo']
                followers_info[i]["companyName"] = experience_data['companyName']
                followers_info[i]["locationName"] = experience_data['location']
            else: followers_info[i]["jobTitle"] = ''
            i += 1
                    
        return followers_info
    
    else:
        print(f"Failed to retrieve followers data")
        return {}
