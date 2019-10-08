# DIRBS View API

Copyright (c) 2018-2019 Qualcomm Technologies, Inc.

All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted (subject to the 
limitations in the disclaimer below) provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this list of conditions and the following 
disclaimer.
* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following 
disclaimer in the documentation and/or other materials provided with the distribution.
* Neither the name of Qualcomm Technologies, Inc. nor the names of its contributors may be used to endorse or promote 
products derived from this software without specific prior written permission.
* The origin of this software must not be misrepresented; you must not claim that you wrote the original software. 
If you use this software in a product, an acknowledgment is required by displaying the trademark/log as per the details 
provided here: https://www.qualcomm.com/documents/dirbs-logo-and-brand-guidelines
* Altered source versions must be plainly marked as such, and must not be misrepresented as being the original software.
* This notice may not be removed or altered from any source distribution.

NO EXPRESS OR IMPLIED LICENSES TO ANY PARTY'S PATENT RIGHTS ARE GRANTED BY THIS LICENSE. THIS SOFTWARE IS PROVIDED BY 
THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE 
 COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
 DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR 
 BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT 
 (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
 POSSIBILITY OF SUCH DAMAGE.
 
 ## Device Identification Registration & Blocking System View (DIRBS-View)
Device Identification, Registration & Blocking System View (DIRBS-View) is a system developed for
the authorized entity (ies) to sight all the information stored in DIRBS and its subsystems via
categorized indicators. DIRBS View provides a platform to visualize the segregated information
based on customized filters which user can set according to the requirements.

### Documentation
[DIRBS-View-User-Guide-v1.0.0.pdf](https://github.com/dirbs/Documentation/tree/master/DIRBS-View/DIRBS-View-User-Guide-v1.0.0.pdf)<br />
[DIRBS-View-Installation-Guide-v1.0.0.pdf](https://github.com/dirbs/Documentation/tree/master/DIRBS-View/DIRBS-View-Installation-Guide-v1.0.0.pdf)<br />
[DIRBS-View-SPA-Installation-Guide-v1.0.0.pdf](https://github.com/dirbs/Documentation/tree/master/DIRBS-View/DIRBS-View-SPA-Installation-Guide-v1.0.0.pdf)<br />


### Frontend Application Repo
https://github.com/dirbs/DIRBS-VIEW-Frontend

### Directory structure
This repository contains code for **D-VIEW** part of the **DIRBS**. It contains
* ``app/`` -- The D-VIEW core server app, to be used as D-VIEW Web Server including database models, apis and resources
* ``mock/`` -- Sample data files etc which are used in app to be reside here
* ``tests/`` -- Unit test scripts and Data
* ``Documentation/`` -- Installation guide for D-VIEW

### Prerequisites
In order to run a development environment, [Python 3.0+](https://www.python.org/download/releases/3.0/) and
[Elastic Stack 6.6.0](https://www.elastic.co/blog/elastic-stack-6-6-0-released) are assumed to be already installed.

We also assume that this repo is cloned from Github onto the local computer, it is assumed that
all commands mentioned in this guide are run from root directory of the project and inside
```virtual environment```

On Windows, we assume that a Bash like shell is available (i.e Bash under Cygwin), with GNU make installed.

### Starting a dev environment
The easiest and quickest way to get started is to use local-only environment (i.e everything runs locally, including
ELK Stack). To setup the local environment, follow the section below:

### Setting up local dev environment
For setting up a local dev environment we assume that the ```prerequisites``` are met already. To setup a local
environment:
* Create database using Elasticsearch (Name and credentials should be same as in [config](/reference-config.yml))
* Create virtual environment using **virtualenv** and activate it:
```bash
virtualenv venv
source venv/bin/activate
```
Make sure that virtual-env is made using Python3 and all the required dependencies are installed.

* Start D-VIEW development server using:
```bash
python run.py
```
This will start a flask development environment for D-VIEW.

* To run unit tests, run:
```bash
pytest -v -s
```
