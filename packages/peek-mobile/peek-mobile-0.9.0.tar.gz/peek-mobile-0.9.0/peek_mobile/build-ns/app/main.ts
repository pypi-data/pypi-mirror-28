// this import should be first in order to load some required settings (like globals and reflect-metadata)
import {platformNativeScriptDynamic} from "nativescript-angular/platform";

// -----------------------------
// Import and set the vortexjs, and the vortex connection
import "nativescript-websockets";
import "moment";

import 'rxjs/add/operator/filter';
import 'rxjs/add/operator/takeUntil';
import 'rxjs/add/operator/first';


// -----------------------------
// Import and set the vortexjs, and the vortex connection
import "@synerty/vortexjs";
import {VortexService} from "@synerty/vortexjs";
VortexService.setVortexUrl(null);

// -----------------------------
// Enable the use of workers for the payload
import {Payload} from "@synerty/vortexjs";
import {PayloadDelegateNs} from "@synerty/vortexjs/index-nativescript";

Payload.setWorkerDelegate(new PayloadDelegateNs());

// -----------------------------
// Enavble the IQ Keyboard
// import  "nativescript-iqkeyboardmanager";
// const iqKeyboard = IQKeyboardManager.sharedManager();
// iqKeyboard.overrideKeyboardAppearance = true;
// iqKeyboard.keyboardAppearance = UIKeyboardAppearance.Dark;

// -----------------------------
// Enable production angular

// import "nativescript-angular";
// // Potentially enable angular prod mode
// import {enableProdMode} from "@angular/core";
// import {environment} from "../src/environments/environment";
//
// if (environment.production) {
//     enableProdMode();
// }


// -----------------------------
// Bootstrap the app
// This should be last
import {AppNsModule} from "./app.ns.module";

platformNativeScriptDynamic().bootstrapModule(AppNsModule);
