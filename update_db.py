import requests


def update_vector_db():
    doctor_count = requests.get("https://healtrip.azurewebsites.net/doctor/count").json()
    hospital_count = requests.get("https://healtrip.azurewebsites.net/hospital/count").json()

    doctors = requests.get("https://healtrip.azurewebsites.net/doctor/getAllForAI").json()
    doctor_description = requests.get("https://healtrip.azurewebsites.net/doctor/getAllDescriptions").json()

    hospitals = requests.get("https://healtrip.azurewebsites.net/hospital/getAll").json()
    hospitals_small_desc = requests.get("https://healtrip.azurewebsites.net/hospital/getAllDescriptions").json()
    hospitals_long_desc = requests.get("https://healtrip.azurewebsites.net/hospital/getAllLongDescriptions").json()



    hotels = requests.get("https://healtrip.azurewebsites.net/hotel/getAllForAI").json()

    # ilkine de virgül koyuyor ona bir bak
    hospital_names = ""
    for hospital in hospitals:
        hospital_names = hospital_names + ", " + hospital["hospitalName"]
    hospitals_small_desc = [hospital for hospital in hospitals_small_desc if hospital is not None]
    hospitals_small_desc_st = "".join(hospitals_small_desc)
    for i, hosp in enumerate(hospitals_long_desc):
        import re
        hospitals_long_desc[i] = re.sub(r'\s+', ' ', hospitals_long_desc[i])

    hospitals_long_desc_st = [hospital for hospital in hospitals_long_desc if hospital is not None]
    hospitals_long_desc_st = "\n\n    ".join(hospitals_long_desc)

    doctor_small_desc = ""
    for doctor in doctors:
        s = doctor["doctorName"] + " with specialty in " + doctor["department"]["departmentName"] + ", "
        doctor_small_desc = doctor_small_desc + s
    doctor_description = [doctor for doctor in doctor_description if doctor is not None]
    doctor_description_st = "".join(doctor_description)

    hotels_desc = ""
    for hotel in hotels:
        hotels_desc = hotels_desc + hotel["description"]

    TEMPLATE = f"""
    There are {doctor_count} doctors in {hospital_count} different hospitals. They are all specialists in their fields. Speciality also mean department. They can receive patients by appointment on certain days of the week. Please contact the hospital directly for an appointment.
    The doctors are {doctor_small_desc}.
    Appointment can be created by contacting the hospital directly. Please contact the hospital directly for an appointment.

    Here are the doctors and their specialties:
    {doctor_description_st}
    
    There are {hospital_count} hospitals and available hospitals are {hospital_names}. These hospitals are located in different cities in Turkey. Each hospital has different departments and specialties. The hospitals are known for their high-quality healthcare services, state-of-the-art facilities, and expert medical staff. Patients can expect to receive personalized care, advanced treatments, and compassionate support at these hospitals.
    {hospitals_small_desc_st}
            
    Here are the hospitals and their detailed information:
    {hospitals_long_desc_st}

    When patient visit the hospital, Patient can stay in the hotel near the hospital.
    There are hotels near each hospital where patients and their families can stay during their treatment. Patients will be planning their trip to Hospitals by considering the close hotels options. Patients can expect to receive world-class care and support at these hospitals, with a focus on personalized treatment plans and positive outcomes. The hospitals are committed to providing the highest quality of care and ensuring that patients have a positive experience during their treatment.

    {hotels_desc}

    Both Akra Hotel and Rixos Hotel offer luxurious accommodations and modern amenities near Medicalpark Hospital in Antalya, Turkey, providing patients and their families with convenient places to stay during treatment. Akra Hotel, situated in the heart of Antalya, boasts of its prime location, offering easy access to popular attractions, shopping centers, and dining options. It provides a peaceful retreat with facilities like a spa, fitness center, and outdoor pool, ensuring a comfortable stay for guests. On the other hand, Rixos Hotel, nestled near the sea, offers a serene environment with stunning views and beachside access, providing guests with a tranquil atmosphere. Both hotels feature a variety of dining options to cater to guests' needs, ensuring a delightful culinary experience. Whether guests prioritize exploring the city or enjoying the scenic beauty near the sea, they can choose between Akra Hotel's central location or Rixos Hotel's beachside ambiance for their stay in Antalya.

    """


    with open("./sources/dhh_db.txt", 'w') as file:
        file.write(TEMPLATE)
