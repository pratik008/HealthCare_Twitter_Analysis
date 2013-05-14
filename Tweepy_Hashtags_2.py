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

    trackList = ['#krankenhaus','#krebs','#kyhc','#laruletadelahorro','#Lasik','#LcChat','#LHH_H2H','#LHI','#LHIN','#lifestylemedicine','#LivingwithMS','#LLABagLadies','#longtermcare','#LTC','#LupusStyle','#malpractice','#mammogram','#mammogram','#mammograms','#mammography','#massagetherapy','#maternalHealth','#maternalMortality','#MayoCIM','#mayoclinic','#mbmed','#mcaidx','#mccfi','#mccsm','#McrFluSafe','#McrMentalHealth','#McrSCR','#MDchat','#MDehr','#MDigitalLife','#MDMLG','#MeaningfulUse','#meatlessmonday','#mecfs','#medApps','#medcomms','#MedDevice','#meded2','#Medicaid','#medical','#medicalbilling','#medicalhome','#medicalimaging','#MedicalMonday','#Medicare','#medicine','#medizin','#MedSafety','#medschool','#medschools','#MedSM','#MedStartr','#medstudent','#MedsUpAway','#medtech','#MeduTOT','#MedXeP','#mefirst','#mentalhealth','#MentalHealthMatters','#mentalhealthmonday','#mentalhealthmonth','#mentalillness','#mgma','#mh4ot','#mhbrain','#mHealth','#mHealthChat','#mHealthZone','#mhm','#mhoz','#midwife','#midwifery','#midwives','#milhealth','#MindfulEating','#miscarriage','#mobilehealth','#modelH','#Montefiore','#Mountaintrauma','#MRI','#MU2','#MyHealth','#myhealthstory','#myplate','#NAPH','#naturalhealth','#NaturalMedicine','#Naturopathic','#NCDchat','#neonatologist','#neonatology','#NephMadness','#Nephrologist','#Nephrology','#Neurologist','#Neurologists','#Neurology','#neuroscience','#Neurosurgeon','#Neurosurgeons','#Neurosurgery','#ngdoc','#nhis','#nhs','#NHSchange','#nhschangeday','#nhsreform','#nhsreforms','#NHSTweets','#NHSXmas','#NIH','#NIVW','#NMAM','#NNM','#novoiceweek','#NowTrending2012','#NPchat','#NPfIT','#NPINchat','#NUR325','#NurFlash','#nurse','#nurses','#nurseshift','#NurseUp','#nursing','#nursinghome','#nurstudent','#nutrition','#NYCHBL','#obgyn','#Obstetrics','#Occhat','#occmatters','#occtherapy','#occupationaltherapy','#occupyhealth','#occupyhealthcare','#od12','#ONC','#ONC','#oncochat','#Oncologist','#Oncologists','#Oncology','#OneLineOneDay','#openEHR','#opengpsoc','#openMRS','#Ophthalmology','#optometry','#OralCancer','#oralhygiene','#OralSurgery','#organdonation','#Orthodontics','#Orthopaedics','#orthopedics','#otolaryngologists','#Otolaryngology','#OTuesday','#ovarianchat','#P2PHC','#PAGuidelines','#pahohealth4change','#palliative','#PALLIchat','#pancreas','#ParaAus','#paramedic','#ParamedicABC','#PartD','#Pathologist','#Pathology','#patient','#patienteducation','#patientengagement','#patientexperience','#PatientNav','#patients','#pbschat','#PCMH','#PCORI','#Pediatric','#Pediatrician','#Pediatricians','#Pediatrics','#pedpc','#pedsurg','#peremendemovement','#Pflege','#pharma','#pharma100','#pharmaceutical','#pharmaceuticals','#pharmacist','#pharmacy','#pharmacynews','#pharmamktg','#pharmaphorum','#phealth','#PHOAMed','#phr','#PHSSR','#phychat','#physicaltherapist','#physicaltherapy','#physician','#physicianassistant','#PhysicianAssistants','#physicians','#PlasticSurgeon','#PlasticSurgeons','#PlasticSurgery','#pm101','#Podiatrist','#Podiatrists','#Podiatry','#poliochat','#PopulationHealth','#PPACA','#practicemanagement','#pregnancychat','#PreSLP','#prevwell','#PrimaryCare','#prostatecare','#protesisdental','#ProtonTherapy','#psych','#Psychiatrist','#Psychiatrists','#Psychiatry','#Psychologie','#Psychologist','#Psychologists','#Psychology','#ptcentcare','#pted','#ptexperience','#PToutcomes','#ptsafety','#ptsafetychat','#ptspkr','#pubhealth','#publichealth','#Pulmonary','#puwebcast','#Qczv','#qic','#QSWB','#QuantifiedSelf','#R2Hchat','#Radiologist','#Radiologists','#Radiology','#RaganSocial','#rareACTION','#RD2Be','#readmissions','#rebif','#recoverychat','#refugeehealth','#rehab','#rehabchat','#rehabilitation','#respirarbien','#respiratory','#respiratorytherapist','#revcycle','#Rheumatologist','#Rheumatology','#rheumedu','#rhumedu','#righttoavoice','#rimasanestesicas','#RN','#RNedu','#ruralhealth','#RuralMed','#RuralMH','#RWJFWeb20','#rxcom','#rxsave','#RXSocial','#s4pm','#sacom','#salu20','#SaudiMedEd','#SaveAbx','#SaveAll','#SCFitFridays','#sdm','#SDMchat','#SDOH','#SDOHchat','#secondvictim','#SegPac','#senior','#seniors','#sensibilidaddental','#sensorychat','#SGReport','#shoyomo','#signagainststroke','#singlepayer','#skincare','#SleepDeprivation','#slp','#SLP2B','#slpchat','#slpeeps','#SLPeeps','#smccg','#sochealth','#socialQI','#SoMeCME','#spedchat','#spine','#Spital','#spoonie','#spoonies','#sportsmedicine','#startuphealth','#stemcell','#strokeoz','#StTwitters','#SubstanceAbuse','#supertwision','#surgeon','#svmed','#SW4HC','#SWLIP','#talkalz','#talkingmentalhealth','#TCK','#TDWI','#teeth','#telecare','#telehealth','#telemedicine','#thcsm','#therapist','#therapy','#therightcare','#thetreasurehunt','#thewalkinggallery','#ThinkIBC','#thyroid','#ticsalut','#transfusion','#Transplantation','#traumaresearch','#tsunamiblanco','#TT4health','#tvlmed','#tweEDers','#twitjc','#UCLAMDChat','#UICC','#ukcare','#ultrasound','#UMCHOP','#UPIM','#urgentcare','#urojc','#Urologist','#Urology','#USPSTF','#vaccination','#vaccines','#VAResearch','#VAResearchWK','#Vasectomy','#vaxfax','#vdgm','#VetoViolence','#VitalSigns','#VMMC','#vschat','#wcphep','#WDD','#WDHD','#wellocracy','#wemidwives','#whatifhc','#whcc','#wheelchair','#wholify','#WhyStopNow','#wirelesshealth','#Withings','#wmnhealth']
    stream = Stream(auth, listener)
    stream.filter(track = trackList)


'''
    for attr, value in status.__dict__.iteritems():
        print attr, ": ", value
'''
