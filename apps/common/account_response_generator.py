def gen_valid_registration_request_data(gender=None, telegram_id=None) -> dict:
    data =  {
        "first_name": "first_name",
        "last_name": "last_name",
        "username": "username",
        "password": "password",
        "email": "danila@gmail.com",
        "phone": "+79999999999",
        "birth_date": "2000-01-01",
    }

    if gender is not None:
        data["gender"] = gender
    if telegram_id is not None:
        data["telegram_id"] = telegram_id

    return data

def gen_invalid_registration_request_data() -> list[dict]:
    valid_data = gen_valid_registration_request_data()

    resp_data_list = []
    for key in valid_data.keys():
        invalid_data = valid_data.copy()
        invalid_data.pop(key)
        resp_data_list.append(invalid_data)

    return resp_data_list

