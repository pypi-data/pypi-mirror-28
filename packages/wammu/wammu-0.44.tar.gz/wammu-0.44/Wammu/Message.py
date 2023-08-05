# -*- coding: UTF-8 -*-
#
# Copyright © 2003 - 2018 Michal Čihař <michal@cihar.com>
#
# This file is part of Wammu <https://wammu.eu/>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''
Wammu - Phone manager
Message reader
'''

import Wammu.Reader
import Wammu.Utils
import Wammu

class GetMessage(Wammu.Reader.Reader):
    def GetStatus(self):
        status = self.sm.GetSMSStatus()
        return status['SIMUsed'] + status['PhoneUsed'] + status['TemplatesUsed']

    def GetNextStart(self):
        return self.sm.GetNextSMS(Start=True, Folder=0)

    def GetNext(self, location):
        return self.sm.GetNextSMS(Location=location, Folder=0)

    def Get(self, location):
        return self.sm.GetSMS(Location=location, Folder=0)

    def Parse(self, value):
        return

    def Send(self, data):
        res = Wammu.Utils.ProcessMessages(data, True)
        self.SendData(['message', 'Read'], res['read'], False)
        self.SendData(['message', 'UnRead'], res['unread'], False)
        self.SendData(['message', 'Sent'], res['sent'], False)
        self.SendData(['message', 'UnSent'], res['unsent'])
