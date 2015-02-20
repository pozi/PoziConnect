<img src="http://i.imgur.com/TLMFPUa.png" alt="Groundtruth" width="200">

# Pozi Connect for M1s

Pozi Connect automatically generates council 'M1' reports that are used for updating the Victorian state map base.

![M1 Form](http://i.imgur.com/rlp9JKS.jpg "M1 Form")

Pozi Connect compares the council's property data with the latest Vicmap data and determines what updates are required in Vicmap to accurately reflect the council's property and address information.

After Groundtruth configures and implements Pozi Connect for your council, you can generate M1s at any time by launching Pozi Connect and running the three or four M1 tasks from the picklist. Your M1 report will be generated to a pre-defined location, and it is ready to be submitted via the [NES](http://nes.land.vic.gov.au/WebSite/Login.aspx) system.

(See Pozi Connect's [history](/poziconnect/m1s/audits) to see the our most recent changes.)

## Preparation

Download and unzip the following MapInfo or SHP datasets to the predefined location on your network:

* Vicmap Address
* Vicmap Property Simplified v1

(If you do not know the predefined locations on your network for these datasets, launch Pozi Connect and pick the M1 task that relates to importing Vicmap. The network location is shown there.)

If you have not already done so, set up a weekly repeat order for both datasets at the [Spatial Datamart]( http://services.land.vic.gov.au/SpatialDatamart/).

## Generating M1s

Launch Pozi Connect. From the picklist, select the first M1 task that relates to your council name:

![Pozi Connect for M1s](http://i.imgur.com/Yx9RH81.png "Pozi Connect for M1s")

For each of the three to four M1 tasks in the picklist:

* select respective M1 item from list
* enter any credentials if prompted (if a username/password is required, enter the *database* credentials)
* click 'Start' (each task will take between half a minute and ten minutes)

There are three or four tasks, depending on whether your council has been configured for importing any custom address locations.

Upon completion of the 'Generate M1' M1 task, you can find the completed M1 report in the `PoziConnect\output\M1` folder.

## Submitting M1

### Preview

Open up the M1 report in Excel to preview the updates that Pozi Connect has generated. Scroll all the way to the right, and review the Comments (column AX) field.

![M1 Comments](http://i.imgur.com/bZz3m1Z.png "M1 Comments")

You may find you want to hold back some updates if you're not sure that you want to submit them. For example, if an update's comments show that a property is going to be added as a multi-assessment and you're not sure that it should be a multi-assessment, you may delete the row before you submit the M1. This gives you the opportunity to check your property system to see if you're happy with affected properties' parcel description (if two properties share the same parcel description, Pozi Connect will assume they are meant to be a multi-assessment).

Any rows you delete will simply appear on the next M1 if there are no changes made to the council's property data.

Other items to look out for:

* warnings (WARNING: conflicting localities): check that you're happy for a property to be allocated to a parcel whose locality differs in Vicmap and Council
* new roads (column AL): if a Council road name doesn't exist in Vicmap, it will assume that the Council road name is correct, and it will be flagged as a 'new road' in Vicmap, and the new road name will be accepted as the official road name; check that it's not a typo

After you've removed any records you don't want to submit, save the spreadsheet with a different name to differentiate it from the original output. You can even save it to a different folder of 'submitted' M1s to keep a record of M1s you've actually submitted (as opposed ones that have been generated but not submitted, say for data cleansing purposes).

### Submit

Log on to [NES](http://nes.land.vic.gov.au/WebSite/Login.aspx) and upload the spreadsheet file as per the [M1 Form Load Guide](http://nes.land.vic.gov.au/WebSite/help/NES_Quick_Guides_-_M1_Form_Load_V1.8.pdf) [pdf].

## Data Audits

[Audits](/poziconnect/m1s/audits)

## Troubleshooting

### Edits are not yet handled by Pozi Connect

* secondary addresses
* multi-assessment properties where all existing propnums in Vicmap are incorrctly matched
* transfers of parcels that contain a primary address
* address position update
