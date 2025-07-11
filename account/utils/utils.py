from datetime import datetime


def profile_to_dict(profile):
    return {
        "firstName": profile.first_name,
        "surname": profile.surname,
        "mobile": profile.mobile,
        "gender": profile.gender,
        "maritusStatus": profile.maritus_status,
        "country": profile.country,
        "state": profile.state,
        "postcode": profile.postcode,
        "identificationDocuments": profile.identification_documents,
        "signature": profile.signature,
}


def current_year_choices(number_of_years_to_create=20):
    current_year = datetime.now().year
    return  [(year, str(year)) for year in range(current_year, current_year + number_of_years_to_create)]