"""
Processes and stores data about Professors in BYU's Religious Education

Classes:
Professor - Store data for a brightspot_employee in BYU's Religious Education.
ProfessorProcessor - Functions used to get BrightSpot brightspot_employee data.

Constants:
RELIGION_DIR_URL - url for Religious Education at BYU
"""

from src.brightspot_employee.employee import *
from src.brightspot_employee.room import Room

from bs4.element import Tag as BeautifulSoup_Tag

from typing import List

RELIGION_DIR_URL = 'https://religion.byu.edu/directory'


class ProfessorProcessor(EmployeeProcessor):
    """
    Functions used to get brightspot_employee data for Religious Education faculty and staff.

    This class assumes html data comes from RELIGION_DIR_URL
    Subclass for use with Professor by setting Professor.processor to a subclass of ProfessorProcessor
    or the processor attribute of a subclass of Professor

    Constants:
    DEFAULT_CONTAINER - Default container for brightspot_employee's to be in within this BrightSpot directory page.

    """

    DEFAULT_CONTAINER = 'PromoVerticalImage'
    DEFAULT_SUPER_CONTAINER = 'ListVerticalImage-items-item'

    def __init__(self, container: str = DEFAULT_CONTAINER, super_container: str = DEFAULT_SUPER_CONTAINER):
        super().__init__(container, super_container)


class Professor(Employee):
    """
    Convenience improvements to Employee to better pull and store information for BYU's Religious Education.

    Class Attributes:
    processor - class used for processing all brightspot_employee fields
    """

    processor = ProfessorProcessor()

    def __init__(self, first_name: str, last_name: str, room_address: Room,
                 page_url: str, telephone: str, department: str, job_title: str):
        super().__init__(first_name, last_name, room_address, page_url, telephone, department, job_title)

    @classmethod
    def from_html_tag(cls: Type[E], tag: BeautifulSoup_Tag) -> Type[E]:
        """
        Create a Professor using a BeautifulSoup tag object.

        :param tag: : BeautifulSoup_Tag containing exactly one brightspot_employee's data
        :return: Professor instance
        """
        return super().from_html_tag(tag)

    @classmethod
    def from_website(cls: Type[E], url: str = RELIGION_DIR_URL) -> List[Type[E]]:
        """
        Return a list of Employee instances using data from the website at url.
        The url is only guaranteed to work at RELIGION_DIR_URL, the default url

        :param url: : webpage to pull all data from
        :return: list of Employee instances from the url's data
        """
        return super().from_website(url)