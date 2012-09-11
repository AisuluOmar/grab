# coding: utf-8
from unittest import TestCase

from grab import Grab, DataNotFound
from grab.container import Container, IntegerField, StringField, DateTimeField
from test.util import GRAB_TRANSPORT

XML = """
<?xml version='1.0' encoding='utf-8'?>
<bbapi version='1'>
    <player id='26982032' retrieved='2012-09-11T07:38:44Z'>
        <firstName>Ardeshir</firstName>
        <lastName>Lohrasbi</lastName>
        <nationality id='89'>Pakistan</nationality>
        <age>19</age>
        <height>75</height>
        <dmi>14300</dmi>
    </player>
</bbapi>
"""

class Player(Container):
    id = IntegerField('//player/@id')
    first_name = StringField('//player/firstname')
    retrieved = DateTimeField('//player/@retrieved', '%Y-%m-%dT%H:%M:%SZ')

    data_not_found = StringField('//data/no/found')

class TestContainers(TestCase):
    def test_container_base_behavior(self):
        grab = Grab(transport=GRAB_TRANSPORT)
        grab.fake_response(XML)

        player = Player(grab)

        self.assertEquals(26982032, player.id)
        self.assertEquals('Ardeshir', player.first_name)
        self.assertEquals('2012-09-11 07:38:44', str(player.retrieved))

        with self.assertRaises(DataNotFound): player.data_not_found
