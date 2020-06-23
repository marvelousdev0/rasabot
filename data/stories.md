## happy path
* greet
  - utter_greet
* mood_great
  - utter_happy

## sad path 1
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* affirm
  - utter_happy

## sad path 2
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* deny
  - utter_goodbye

## say goodbye
* goodbye
  - utter_goodbye

## bot challenge
* bot_challenge
  - utter_iamabot

## interactive_story_1
* employee_first_name
    - utter_employee_first_name
    - form_employee_first_name
    - form{"name": "form_employee_first_name"}
    - slot{"requested_slot": "employee_id"}
* form: affirm{"emp_id": "EMP001"}
    - form: form_employee_first_name
    - slot{"employee_id": "EMP001"}
    - form{"name": null}
    - slot{"requested_slot": null}

## interactive_story_1
* check_basic_api
    - action_check_basic_api

## interactive_story_1
* list_employees
    - utter_list_employees
    - form_employee_job_title
    - form{"name": "form_employee_job_title"}
    - slot{"requested_slot": "job_title"}
* form: affirm{"designation": "District Directives Developer"}
    - form: form_employee_job_title
    - slot{"job_title": "District Directives Developer"}
    - form{"name": null}
    - slot{"requested_slot": null}

## interactive_story_1
* employee_details{"emp_id": "EMP001"}
    - action_employee_details

## interactive_story_1
* check_weather_location{"location_name": "Chicago"}
    - action_check_weather

## interactive_story_1
* check_weather
    - utter_request_location
    - form_action_check_weather
    - form{"name": "form_action_check_weather"}
    - slot{"requested_slot": "location"}
* form: affirm{"location_name": "San Francisco"}
    - form: form_action_check_weather
    - slot{"location": "San Francisco"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_check_weather
