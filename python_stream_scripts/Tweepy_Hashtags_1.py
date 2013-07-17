#Read About tweepy at http://pythoncentral.org/introduction-to-tweepy-twitter-for-python/

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import tweepy

config_json = open('config.json', 'r')
config = json.load(config_json)

print 

# Go to http://dev.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key    = config["consumer_key"]
consumer_secret = config["consumer_secret"]

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token = config["access_token"]
access_token_secret = config["access_token_secret"]


class StdOutListener(StreamListener):
    ''' Handles data received from the stream. '''

    def on_status(self, status):
        # Prints the text of the tweet

        print('Tweet text: ' + status.text.encode('utf-8'))
        directAttrs = 'place,coordinates,lang,created_at,retweeted_status,source source_url'.split(',')
        for k in directAttrs:
            value = getattr(status, k, None)
            if value is not None:
                print k, str(value).encode('utf-8')
        userAttrs = 'screen_name,location'.split(',')
        for k in userAttrs:
            value = getattr(status, k, None)
            if value is not None:
                print k, str(value).encode('utf-8')

        return True

    def on_error(self, status_code):
        print('Got an error with status code: ' + str(status_code))
        return True  # To continue listening

    def on_timeout(self):
        print('Timeout...')
        return True  # To continue listening

if __name__ == '__main__':
    listener = StdOutListener()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    trackList = ['#1care','#1in33chat','#1in6','#2WC','#3orMore','#6Cs','#6CsLive','#AACaware','#AACchat','#aacr','#aade','#AAFP','#aao_ophth','#abcfadv','#abhealth','#Abnehmen','#acadsurg','#access2care','#ACLM','#acmhn','#ACO','#ACOchat','#ACOGChat','#ACOs','#ACRP','#acupuncture','#adelgazar','#adherence','#AF4Q','#AFHealthChat','#afmc','#agedcare','#Aging2','#aginginplace','#AHEC','#AHPRA','#AHPScot','#AHRQIX','#ahsn','#Allergist','#Allergists','#ALS','#AlternativeMedicine','#AltMed','#AlzBooks','#AlzFacts','#AmbJC','#amssm','#anaesthesia','#anesthesia','#Anesthesiologist','#Anesthesiology','#anticoagulants','#antidiet','#aphasia','#aprimaria','#APRNchat','#AskTEDMED','#assistivetech','#AtrialFibrillation','#audiology','#audpeeps','#augcomm','#AusMed','#AwDC','#bariatric','#BCHC','#BCMBeats','#beahero','#beanorgandonor','#BestNursingHomes','#betteraccess','#bgnow','#BHSM','#bioethics','#bioethics','#biometrics','#biosimilars','#biotech','#birthgenius','#BleedingDisorders','#BlkBFing','#bluebutton','#blueheelsociety','#bluejc','#BMCMed','#BodyChat','#BOTOX','#BowelCancer','#BrainTumourThursday','#breastfeeding','#bRfchat','#BTSM','#cafescientifique','#CAMHS','#CancerFreeMe','#cancersupport','#candoc','#Cardiologist','#Cardiologists','#Cardiology','#caregiver','#caregivers','#Caremakers','#carepathway','#Carerx','#carnavalsalud','#carteradeservicios','#casemanagement','#cbhceu','#cchleaders','#CDCarthritis','#CDCasthma','#CDCCancerChat','#CDCchat','#CDCcontagion','#CDCEarthDay','#CDCfluchat','#CDCgrandrounds','#CDCsalud','#CDCtips','#cdfmed','#CdnHealth','#CDoM','#celltherapy','#CervicalCA','#CFSAC','#chaocajitafeliz','#ChatDDS','#CHC','#CHCs','#chiropractic','#ChooseWellMcr','#choosingwisely','#chronicallyawesome','#circumchat','#clevelandclinic','#ClinicalNegligence','#clinicalresearch','#clinicaltrials','#CMAHCT','#CMEchat','#CMS','#cochrane','#CochraneEvidence','#CodeSTEMI','#cohcr','#cohiex','#COHRC','#ColonIrritable','#ColonIrritable','#concussion','#contraception','#converses','#cosasdefisio','#COTSS','#co_health','#cpjc','#CPR','#crowdHC','#CruelMystery','#CryoGroup','#cwsccg','#cymh','#dejardefumar','#dental','#dentist','#dentists','#Dermatologist','#Dermatologists','#Dermatology','#dfwhimss','#DiabetesHoy','#Diabetiker','#dietitian','#dietitians','#diferencia_T','#digitalmedicine','#DigPharm','#disease','#docglobal','#doctor','#doctors','#doula','#Dr4A','#drimpy','#DrugInfoAssn','#dryeye','#DXerror','#dysphagia','#E4Eeccw','#EAAD','#EASD','#eatright','#ebm','#ECDC','#ecuimres','#edema','#EGPRN','#eHealth','#ehealth100','#ehealthtalks','#ehr','#EHRbacklash','#eldercare','#embarazo','#embryology','#emr','#ems','#EMTOT','#endoscopy','#EndStigma','#epatient','#epatientgr','#epatients','#epharma','#epigenetics','#eprescribing','#eRx','#esalud','#esaludcyl','#esante','#esoebu','#eutobacco','#eyetips','#FamMedChat','#FDA','#FDAApps','#FDAsm','#fertility','#firstMRI','#fisiolibrooro','#fisiopildora','#fitbit','#FlightEMS','#flufighter','#flushot','#FMRevolution','#FOAMed','#FQHC','#FQHCresearch','#FumbleFriday','#futuremed','#futureofhealth','#FutureOfHealthCare','#gasclass','#Gastroenterology','#gecb','#GEHealthcare','#genomics','#geriatric','#geriatrics','#gerontologie','#gesund','#gesundheit','#Gesundheit','#GetFit','#GetInOnIt','#GFchat','#giftoflife','#gimh','#GivingVoiceUK','#globalhealth','#GlutenFree','#gmcsm','#GMEP','#GoUnDiet','#gratefulmed','#GratefulMedChat','#greatchallenges','#greekpharmacy','#grooteschuur','#Gynecologist','#Gynecology','#H2NYC','#handhygiene','#havethechat','#HCAHPS','#HCAI','#HCbuzzword','#hcinno','#hcit','#hcitin','#hcmkg','#hcmktg','#hcpr','#hcr','#hcsmasia','#hcsmat','#hcsmeu','#hcsmeuES','#hcsmglobal','#hcsmin','#HCSMReview','#hcsmse','#hcsmSV','#hcsmua','#hcsmvac','#hcxns','#health20','#health2dev','#Health2Dublin','#healthapps','#healthcare','#healthcarebusiness','#HealthCareforAll','#HealthcareQA','#healthchat','#healthclaims','#HealthCosts','#healthdata','#healthdisparities','#healtheconomics','#healthequity','#healthinnovations','#healthinsurance','#HealthIT','#healthlaw','#healthlit','#healthliteracy','#healthpolicyvalentines','#HealthQI','#healthrankings','#healthreform','#healthtech','#HealthyChicago','#healthyu','#heartmonth','#heartsurgery','#hearttransplant','#Hematology','#HEOR','#HerpesChat','#herpeslabial','#HESP','#HHS','#HHSHAI','#HIAP','#HIE','#himss','#HIPAA','#histmed','#HIT100','#HITchicks','#HITedu','#HITplan','#HITpm','#HITpol','#hitsc','#HITstd','#HIX','#HL7','#hlbc','#hmenews','#hmo','#homecare','#homehealth','#homehealthcare','#hospice','#hospital','#hospitals','#howmuchisthat','#hpmmd','#hsc6935','#HTChat','#hvhcf','#hwbbu','#iami','#IBCLC','#ICD10','#ICD11','#ICD9','#iDoctus','#idpdchat','#imaging','#immunotherapy','#IMPX','#IndigenousHealth','#infant','#infectiousdisease','#InnoRx','#insulinpump','#IntegrativeMedicine','#interncrisis','#Internist','#interstim','#intuitiveeating','#ISQuachat','#IUHedu','#IUHedu','#IUPedsGrRounds','#ivf','#JC_StE','#JDRF','#jhhgr','#kickcancer','#KidsHealth','#kneereplacement','#kpcthblog','#KPSM']
    stream = Stream(auth, listener)
    stream.filter(track = trackList)


'''
    for attr, value in status.__dict__.iteritems():
        print attr, ": ", value
'''
