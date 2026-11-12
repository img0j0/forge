import UIKit
import Capacitor

// The app's web view controller: Capacitor's own, plus Forgelings' local plugins.
class MainViewController: CAPBridgeViewController {
    override open func capacitorDidLoad() {
        bridge?.registerPluginInstance(CloudSavePlugin())
    }
}
