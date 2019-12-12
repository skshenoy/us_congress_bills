# US Congress Bills
Exploring bulk data on US Congress bills, compiled by ProPublica and the @UnitedStates GitHub organization. Thanks to House Appropriations!

> “At the direction of the U.S. House of Representatives Appropriations Committee, in support of the Legislative Branch Bulk Data Task Force, the Government Publishing (GPO), the Library of Congress (LOC), the Clerk of the House, and the Secretary of the Senate are making Bill Status information in XML format available through the GPO’s Bulk Data repository starting with the 113th Congress.”

This project looks into the bulk bill data of the 115th US Congress, in session from January 2017 to January 2019. A large part of this project is descriptive statistics surrounding the rate of passage of bills, the sponsorship and cosponsorship records, the subjects of the bills, and the titles of the bills, among other fields.

Much of this exploration culminated in a Dash-based web app, soon to be hosted publicly, where you can select individual legislators take a deep dive into their work as part of the 115th Congress.

The rest of this project aimed at predicting whether a bill would pass or not, using a variety of different features including:
- sponsors (and party)
- number of cosponsors (from each party)
- bill's top subject
- bill's official title
- number of amendments
- number of related bills

The outcome of this portion of the project is displayed on the second page of the web app, where you can make up a bill and see if the final model predicts that it will pass or not.
