# STO-server
Backend repository for Web application Safe-TakeOff by flake inc. 

The project's major objective is to forecast weather so that flights can be planned to take off and
land safely. A model will be developed to forecast the weather for a specific day using time series data
from the oikolab weather dataset. The predicted weather conditions will be used to decide if a specific
flight can take off or land where the dataset was recorded.
A web application will be developed with a dashboard which has the functionality to check for
the weather conditions for a given date.The dashboard will show the weather for today, the planes that
can take off today, and graphs of the weather for the preceding month, etc. Additionally, the program
will be able to forecast weather for a certain area using a different dataset from a different place that
contains the same data columns as the oikolab dataset. A dataset can be imported from the user interface
for this.
In order to make the major prediction, you must first choose the kind of aeroplane you are
interested in (Aeroplane types are predefined). You then need to enter the target date for your check.
Following submission, the outcome will be shown on the screen together with information about the
weather conditions and whether this particular flight can or cannot takeoff/land from this location.
Additionally, the system can be expanded to accommodate additional aircraft types. The
aeroplane's thresholds must be included when adding the aircraft. (For instance, a commercial aircraft
can withstand winds up to 50 km/h without having an impact on takeoff.)
