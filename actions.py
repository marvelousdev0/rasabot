# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

from typing import Any, Text, Dict, List, Union, Optional
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import Restarted, SlotSet, AllSlotsReset
import requests
import json
import re
import weatherApi
import employeesApi
import stockApi


class FormEmployeeFirstName(FormAction):
    def name(self):
        return "form_employee_first_name"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["employee_id"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {"employee_id": [self.from_text()]}

    @staticmethod
    def employee_id_format() -> List[Text]:
        return ["EMP001"]

    def validate_employee_id(self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> Optional[Text]:
        if value in self.employee_id_format():
            return {"employee_id": value}
        else:
            dispatcher.utter_message(template="utter_wrong_employee_id")
            return {"employee_id": None}

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict]:
        dispatcher.utter_message(template="utter_employee_id_successful")
        return []


class FormEmployeeJobTitle(FormAction):
    def name(self):
        return "form_employee_job_title"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["job_title"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {"job_title": [self.from_text()]}

    @staticmethod
    def job_title_format() -> List[Text]:
        return ["District Directives Developer"]

    def validate_job_title(self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> Optional[Text]:
        if value in self.job_title_format():
            return {"job_title": value}
        else:
            dispatcher.utter_message(text="Wrong job title provided!")
            return {"job_title": None}

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict]:
        dispatcher.utter_message(template="utter_job_title_successful")
        return []


class EmployeeDetails(Action):
    def name(self):
        return "action_employee_details"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict]:
        employeeid = next(tracker.get_latest_entity_values("emp_id"), None)
        print(employeeid)
        if (employeeid is None):
            dispatcher.utter_template("utter_ask_employee_id", tracker)
        else:
            employee_details = employeesApi.getEmployeeDetails(employeeid)
            if (employee_details is None):
                dispatcher.utter_message(
                    "Sorry, I couldn't get employee details")
            else:
                messageToUser = "Employee name is {} {}".format(
                    employee_details['data']['firstName'], employee_details['data']['lastName'])
                dispatcher.utter_message(messageToUser)
        return []


class checkApiFunctionality(Action):
    def name(self):
        return "action_check_basic_api"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict]:
        response = requests.get("https://jsonplaceholder.typicode.com/todos/1")
        jsonResponse = response.json()
        title = jsonResponse["title"]
        id = jsonResponse["id"]

        messageToUser = "The user id is {} and title is {}. And this is coming from an api call.".format(
            id, title)
        dispatcher.utter_message(messageToUser)
        return []


class ActionCheckWeather(Action):
    def name(self):
        return "action_check_weather"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict]:
        location_slot = str(tracker.get_slot('location'))
        location_entity = next(
            tracker.get_latest_entity_values('location_name'), None)
        location = ""
        if (location_entity is None):
            location = location_slot
        else:
            location = location_entity
        data = stockApi.getStockData()
        print(data)
        current_conditions = weatherApi.getWeatherByLocation(location)
        if(current_conditions is None):
            dispatcher.utter_message("Sorry I couldn't get weather info")
            return []
        else:
            messageToUser = "Temperature currently in {} is {}F. It is {} {} and feels like {}. UV index is {}.".format(
                current_conditions["location"]["name"], current_conditions["current"]["temperature"], current_conditions["current"]["weather_descriptions"][0], current_conditions["current"]["weather_icons"], current_conditions["current"]["feelslike"], current_conditions["current"]["uv_index"])
            # dispatcher.utter_message(messageToUser)
            message = {"payload": "weather", "data": current_conditions}
            dispatcher.utter_message(json_message=message)
            return [SlotSet("location", None)]


class FormCheckWeather(FormAction):
    def name(self):
        return "form_action_check_weather"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["location"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {"location": [self.from_text()]}

    @staticmethod
    def location_format() -> List[Text]:
        return ["San Francisco"]

    def validate_location(self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> Optional[Text]:
        location = tracker.get_slot("location")
        print(location, value)
        if (location is None):
            if value:
                return {"location": value}
            else:
                dispatcher.utter_message(text="Please provide a location")
                return {"location": None}
        else:
            return {"location": value}

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict]:
        return []

class ActionGetStockData(Action):
    def name(self):
        return "action_get_stock_data"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict]:
        stock_symbol_slot = str(tracker.get_slot('stock_symbol_slot'))
        stock_symbol_entity = next(
            tracker.get_latest_entity_values('stock_symbol_entity'), None)
        stock_symbol = ""
        if (stock_symbol_entity is None):
            location = stock_symbol_slot
        else:
            location = stock_symbol_entity
        stock_data = stockApi.getStockData()
        if(stock_data is None):
            dispatcher.utter_message("Sorry I couldn't get stock info")
            return []
        else:
            message = {"payload": "stock", "data": stock_data}
            dispatcher.utter_message(json_message=message)
            return [SlotSet("stock_symbol_slot", None)]


class FormGetStockSymbol(FormAction):
    def name(self):
        return "form_get_stock_symbol"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["stock_symbol_slot"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {"stock_symbol_slot": [self.from_text()]}

    @staticmethod
    def location_format() -> List[Text]:
        return ["AAPL", "IBM"]

    def validate_stock_symbol(self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> Optional[Text]:
        stock_symbol_slot = tracker.get_slot("stock_symbol_slot")
        if (stock_symbol_slot is None):
            if value:
                return {"stock_symbol_slot": value}
            else:
                dispatcher.utter_message(text="Please provide a stock symbol")
                return {"stock_symbol_slot": None}
        else:
            return {"stock_symbol_slot": value}

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict]:
        return []
