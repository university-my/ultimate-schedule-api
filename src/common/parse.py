from collections import namedtuple

from bs4 import BeautifulSoup

from src.common.errors import ParsingError

base_lesson = namedtuple("Base", ["date", "verb", "lessons"])
lesson = namedtuple("Lesson", ["number", "start", "stop", "description", "html"])


def serialize(data):
    schedule = []
    for base in data:
        payload = {"date": base.date, "verbose": base.verb, "lessons": []}
        for single in base.lessons:
            payload["lessons"].append(
                {
                    "number": single.number,
                    "from": single.start,
                    "to": single.stop,
                    "description": single.description,
                    "html": single.html
                }
            )
        schedule.append(payload)

    return schedule


def collect(containers):
    result = []
    for container in containers:
        lessons = []

        # `date` should contains array like this `['29.03.2021', 'Понеділок']`
        # But sometimes `h4` tag may contains more data
        # So I'm getting first two elements from `h4`
        # It works for now :)
        date_and_day = container.h4.text.split()
        date = [date_and_day[0], date_and_day[1]]

        for each_tr in container.find_all("tr"):
            row = each_tr.find_all("td")
            if row[-1].get_text(strip=True):
                html = row[2].encode()
                description = row[2].text.replace("\xa0", " ")
                lesson_time = row[1].text[:5], row[1].text[5:]
                lessons.append(lesson(row[0].text, *lesson_time, description, html))
        result.append(base_lesson(*date, lessons))
    return serialize(result)


def parse(content):
    try:
        soup = BeautifulSoup(content, "lxml").find_all("div", class_="container")
        containers = soup[1].find_all("div", class_="col-md-6")
        if not containers:
            return []
        return collect(containers)
    except LookupError:
        raise ParsingError(
            "Schedule parsing error. Try to fix the X-Schedule-Url header."
        ) from None


def parse_faculties(content: str) -> list:
    """
    Args:
        content (str): Request response body
    Returns:
        list[dict]: list of the faculties codes and names
    """
    soup = BeautifulSoup(content, "lxml")
    form_field = soup.find("select", id="faculty")
    options = form_field.find_all("option")[1:]
    faculties_list = []
    for option in options:
        faculties_list.append({"name": option.text, "code": int(option["value"])})

    return faculties_list
