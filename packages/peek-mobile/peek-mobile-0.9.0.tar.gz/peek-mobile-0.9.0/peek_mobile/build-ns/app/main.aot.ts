// this import should be first in order to load some required settings (like globals and reflect-metadata)
import { platformNativeScript } from "nativescript-angular/platform-static";


import "nativescript-websockets";
import "rxjs/add/operator/filter";
import "moment";

// Import some stuff that we need
import "@synerty/vortexjs";

import {VortexService} from "@synerty/vortexjs";
VortexService.setVortexUrl(null);

// Enable the use of workers for the payload
import {Payload} from "@synerty/vortexjs";
import {PayloadDelegateNs} from "@synerty/vortexjs/index-nativescript";

Payload.setWorkerDelegate(new PayloadDelegateNs());

import { AppModuleNgFactory } from "./app.module.ngfactory";

platformNativeScript().bootstrapModuleFactory(AppModuleNgFactory);
