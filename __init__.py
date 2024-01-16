from adapt.intent import IntentBuilder
from neon_utils.skills.neon_skill import NeonSkill
from ovos_utils import classproperty
from ovos_utils.process_utils import RuntimeRequirements

from mycroft.intent import intent_handler
from mycroft.util.parse import extract_number
from .ql800Printer import Printer
from datetime import datetime

from mycroft.skills.core import intent_handler

class PrintLabel(NeonSkill):
    @classproperty
    def runtime_requirements(self):
        return RuntimeRequirements(network_before_load=False,
                                   internet_before_load=False,
                                   gui_before_load=False,
                                   requires_internet=False,  
                                   requires_network=False,
                                   requires_gui=False,
                                   no_internet_fallback=True,
                                   no_network_fallback=True,
                                   no_gui_fallback=True)

    @intent_handler(IntentBuilder('PrintLabelsIntent')
                    .require('PrintKeyword').require('LabelKeyword'))
    def handle_print_labels_intent(self, message):
        date = datetime.today().strftime('%m/%d/%Y')
        self.log.info(date)

        # testing extract_number
        utt = message.data.get('utterance')
        self.log.info("!BR - " + utt)  # Diagnostic
        offsetLabel = utt.find("label")
        possibleQtyText = utt[:offsetLabel]
        self.log.info("Possible qty text: " + possibleQtyText)
        qty = int(extract_number(possibleQtyText))
        if qty == 0:
          # Check for 'to' instead of 'two' and 'for' instead of 'four'
          if possibleQtyText.find("to") >= 0:
            qty = 2
          elif possibleQtyText.find("for") >= 0:
            qty = 4
          else:
            qty = 1
          pass
        self.log.info(qty)
        # Check for description which begins with "for" after "label(s)"
        postLabelText = utt[offsetLabel + 5:]
        offsetFor = postLabelText.find("for")
        if (offsetFor > -1):
           description = postLabelText[offsetFor+4:]
           description = description.upper()
           self.log.info(description)  # Diagnostic
           self.printer.printLabelTwoLines(date, description, qty)
        else:
           self.printer.printLabelOneLine(date, qty)
           pass

    def stop(self):
        pass


# def create_skill():
#    return PrintLabel()


