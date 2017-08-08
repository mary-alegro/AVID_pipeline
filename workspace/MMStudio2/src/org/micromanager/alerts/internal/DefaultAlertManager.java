///////////////////////////////////////////////////////////////////////////////
//PROJECT:       Micro-Manager
//-----------------------------------------------------------------------------
//
// AUTHOR:       Chris Weisiger, 2016
//
// COPYRIGHT:    (c) 2016 Open Imaging, Inc.
//
// LICENSE:      This file is distributed under the BSD license.
//               License text is included with the source distribution.
//
//               This file is distributed in the hope that it will be useful,
//               but WITHOUT ANY WARRANTY; without even the implied warranty
//               of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
//
//               IN NO EVENT SHALL THE COPYRIGHT OWNER OR
//               CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
//               INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES.
//

package org.micromanager.alerts.internal;

import java.util.HashMap;
import javax.swing.JComponent;
import org.micromanager.Studio;
import org.micromanager.alerts.Alert;
import org.micromanager.alerts.AlertManager;
import org.micromanager.alerts.UpdatableAlert;
import org.micromanager.internal.MMStudio;

public final class DefaultAlertManager implements AlertManager {

   private static final DefaultAlertManager staticInstance_;
   static {
      staticInstance_ = new DefaultAlertManager(MMStudio.getInstance());
   }

   private final Studio studio_;
   private final HashMap<String, CategorizedAlert> titleToCategorizedAlert_ = 
           new HashMap<String, CategorizedAlert>();
   private final HashMap<String, DefaultAlert> titleToCustomAlert_ = 
           new HashMap<String, DefaultAlert>();

   private DefaultAlertManager(Studio studio) {
      studio_ = studio;
   }

   @Override
   public UpdatableAlert postUpdatableAlert(String title, String text) {
      return AlertsWindow.addUpdatableAlert(studio_, title, text);
   }

   @Override
   public Alert postAlert(String title, Class<?> category, String text) {
      CategorizedAlert alert;
      if (titleToCategorizedAlert_.containsKey(title) &&
            titleToCategorizedAlert_.get(title).isUsable()) {
         alert = titleToCategorizedAlert_.get(title);
      }
      else {
         // Make a new Alert to hold messages.
         alert = AlertsWindow.addCategorizedAlert(studio_, title);
         titleToCategorizedAlert_.put(title, alert);
      }
      AlertsWindow.showWindowUnlessMuted(studio_, alert);
      alert.addText(category, text);
      return alert;
   }

   @Override
   public UpdatableAlert postCustomAlert(String title, JComponent contents) {
      if (titleToCustomAlert_.containsKey(title) &&
            titleToCustomAlert_.get(title).getContents() == contents) {
         // Already have this alert.
         return titleToCustomAlert_.get(title);
      }
      DefaultAlert alert = AlertsWindow.addCustomAlert(studio_, title, contents);
      // TODO: this potentially replaces an existing alert.
      titleToCustomAlert_.put(title, alert);
      return alert;
   }

   public static DefaultAlertManager getInstance() {
      return staticInstance_;
   }
}
