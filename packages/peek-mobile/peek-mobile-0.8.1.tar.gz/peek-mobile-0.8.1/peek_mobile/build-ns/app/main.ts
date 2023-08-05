// this import should be first in order to load some required settings (like globals and reflect-metadata)
import {platformNativeScriptDynamic} from "nativescript-angular/platform";

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

// import "nativescript-angular";
// // Potentially enable angular prod mode
// import {enableProdMode} from "@angular/core";
// import {environment} from "../src/environments/environment";
//
// if (environment.production) {
//     enableProdMode();
// }
// This should be last
import {AppNsModule} from "./app.ns.module";

platformNativeScriptDynamic().bootstrapModule(AppNsModule);
