///////////////////////////////////////////////////////////////////////////////
//PROJECT:       Micro-Manager
//SUBSYSTEM:     mmstudio
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


import com.google.common.eventbus.Subscribe;
import java.awt.Font;
import java.awt.Toolkit;
import java.awt.datatransfer.Clipboard;
import java.awt.datatransfer.StringSelection;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.ArrayList;
import java.util.HashSet;
import javax.swing.JButton;
import javax.swing.JCheckBox;
import javax.swing.JComponent;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.SwingUtilities;
import net.miginfocom.swing.MigLayout;
import org.micromanager.Studio;
import org.micromanager.events.internal.InternalShutdownCommencingEvent;
import org.micromanager.internal.utils.MMFrame;



public final class AlertsWindow extends MMFrame {
   private static AlertsWindow staticInstance_;
   private static void ensureWindowExists(Studio studio) {
      if (staticInstance_ == null) {
         staticInstance_ = new AlertsWindow(studio);
         studio.events().registerForEvents(staticInstance_);
      }
   }

   /**
    * Display the AlertsWindow, creating it if necessary.
    * @param studio MM Studio instance
    */
   public static void show(Studio studio) {
      ensureWindowExists(studio);
      if (!staticInstance_.isVisible()) {
         // both of the following methods bring focus to the Alerts Window,
         // which is highly annoying while working on something else.
         // At the risk of making it harder to notice new alerts, I prefer 
         // to call these only when the window is not yet visible.
         staticInstance_.setVisible(true);
         staticInstance_.toFront();
      }
   }

   /**
    * Display the AlertsWindow, if the given alert is not muted.
    * @param studio Studio instance
    * @param alert  Alert to be shown
    */
   public static void showWindowUnlessMuted(Studio studio, DefaultAlert alert) {
      ensureWindowExists(studio);
      if (staticInstance_.isMuted(alert) || !staticInstance_.shouldShowOnMessage_) {
         return;
      }
      show(studio);
   }

   /**
    * Create a simple alert with a text message.
    * @param studio Studio instance
    * @param title  Title of the alert
    * @param text   Text of the alert
    * @return       Alert
    */
   public static DefaultAlert addUpdatableAlert(Studio studio, String title,
         String text) {
      ensureWindowExists(studio);
      DefaultAlert alert = new DefaultAlert(staticInstance_, title,
            new JLabel(text));
      showWindowUnlessMuted(studio, alert);
      staticInstance_.addAlert(alert);
      return alert;
   }

   /**
    * Create a custom alert with any contents
    * @param studio Studio instance
    * @param title  Title of the alert
    * @param contents Content to be added to the alert
    * @return 
    */
   public static DefaultAlert addCustomAlert(Studio studio, String title,
         JComponent contents) {
      ensureWindowExists(studio);
      DefaultAlert alert = new DefaultAlert(staticInstance_, title, contents);
      showWindowUnlessMuted(studio, alert);
      staticInstance_.addAlert(alert);
      return alert;
   }

   /**
    * Create an alert that can contain multiple categories of messages.
    * @param studio Studio instance
    * @param title  Title of the alert
    * @return   Categorized alert
    */
   public static CategorizedAlert addCategorizedAlert(Studio studio, String title) {
      ensureWindowExists(studio);
      CategorizedAlert alert = CategorizedAlert.createAlert(staticInstance_, title);
      showWindowUnlessMuted(studio, alert);
      staticInstance_.addAlert(alert);
      return alert;
   }

   private static final String NO_ALERTS_MSG = "There are no messages at this time.";
   private static final String SHOULD_SHOW_WINDOW = "Show the Messages window when a message is received";

   private Studio studio_;
   private final ArrayList<DefaultAlert> allAlerts_ = new ArrayList<DefaultAlert>();
   private final HashSet<String> mutedAlerts_ = new HashSet<String>();
   private final JPanel alertsPanel_ = new JPanel(new MigLayout("insets 0, fill, flowy"));
   private boolean shouldShowOnMessage_ = true;

   private AlertsWindow(Studio studio) {
      super("Messages");
      studio_ = studio;

      super.loadAndRestorePosition(300, 100);
      
      super.setLayout(new MigLayout("fill, insets 2, gap 0"));

      Font defaultFont = new Font("Arial", Font.PLAIN, 10);

      shouldShowOnMessage_ = studio_.profile().getBoolean(AlertsWindow.class,
            SHOULD_SHOW_WINDOW, true);
      final JCheckBox showWindowCheckBox = new JCheckBox(
            "Open this window when messages arrive", shouldShowOnMessage_);
      showWindowCheckBox.setFont(defaultFont);
      showWindowCheckBox.addActionListener(new ActionListener() {
         @Override
         public void actionPerformed(ActionEvent e) {
            shouldShowOnMessage_ = showWindowCheckBox.isSelected();
            studio_.profile().setBoolean(AlertsWindow.class,
               SHOULD_SHOW_WINDOW, shouldShowOnMessage_);
         }
      });
      super.add(showWindowCheckBox, "split, span");

      JButton clearAllButton = new JButton("Clear All");
      clearAllButton.setFont(defaultFont);
      clearAllButton.setToolTipText("Dismiss all alerts, removing them from this window.");
      clearAllButton.addActionListener(new ActionListener() {
         @Override
         public void actionPerformed(ActionEvent e) {
            // Reverse iteration because we're modifying allAlerts_ as we
            // iterate over it.
            for (int i = allAlerts_.size() - 1; i >= 0; --i) {
               allAlerts_.get(i).dismiss();
            }
         }
      });
      super.add(clearAllButton, "split 2, gapleft push");
      
      // not great to put this next to the Clear button....
      JButton copyButton = new JButton("Copy All");
      copyButton.setFont(defaultFont);
      copyButton.setToolTipText("Copies the content of all alerts");
      copyButton.addActionListener(new ActionListener() {
         @Override
         public void actionPerformed(ActionEvent ae) {
            String text = "";
            for (DefaultAlert alert : allAlerts_) {
               text += alert.getTitle() + System.getProperty("line.separator");
               if (alert instanceof CategorizedAlert) {
                  CategorizedAlert cAlert = (CategorizedAlert) alert;
                  text += cAlert.getAllText();
               } else {
                  text += alert.getText();
               }
               text += System.getProperty("line.separator");
            }
            StringSelection stringSelection = new StringSelection(text);
            Clipboard clpbrd = Toolkit.getDefaultToolkit().getSystemClipboard();
            clpbrd.setContents(stringSelection, null);
         }
      } );
      
      super.add(copyButton, "wrap");

      JScrollPane scroller = new JScrollPane(alertsPanel_,
            JScrollPane.VERTICAL_SCROLLBAR_AS_NEEDED,
            JScrollPane.HORIZONTAL_SCROLLBAR_NEVER);
      scroller.setBorder(null);
      alertsPanel_.add(new JLabel(NO_ALERTS_MSG));
      super.add(scroller, "push, grow");
      super.pack();
   }

   public void addAlert(DefaultAlert alert) {
      if (allAlerts_.isEmpty()) {
         // Remove the "there are no alerts" label.
         alertsPanel_.removeAll();
         alertsPanel_.revalidate();
      }
      allAlerts_.add(alert);
      alertsPanel_.add(alert, "pushx, growx, gaptop 0, gapbottom 0");
      studio_.events().post(new AlertUpdatedEvent(alert));
      packLater();
   }

   public void removeAlert(DefaultAlert alert) {
      if (allAlerts_.contains(alert)) {
         allAlerts_.remove(alert);
         alertsPanel_.remove(alert);
         if (allAlerts_.isEmpty()) {
            studio_.events().post(new NoAlertsAvailableEvent());
            alertsPanel_.add(new JLabel(NO_ALERTS_MSG));
         }
         alertsPanel_.revalidate();
         studio_.events().post(new AlertClearedEvent(alert));
      }
      packLater();
   }

   // HACK: for some reason, packing immediately often results in layout
   // errors, so we wait to pack until a later pass by the EDT.
   private void packLater() {
      SwingUtilities.invokeLater(new Runnable() {
         @Override
         public void run() {
            pack();
         }
      });
   }

   /**
    * Muted alerts won't cause the window to be shown when they appear.
    * @param alert  Alert to be muted or unmuted
    * @param isMuted  Whether or not we want this alert to be muted
    */
   public void setMuted(DefaultAlert alert, boolean isMuted) {
      if (isMuted) {
         mutedAlerts_.add(alert.getTitle());
      }
      else if (mutedAlerts_.contains(alert.getTitle())) {
         mutedAlerts_.remove(alert.getTitle());
      }
   }

   public boolean isMuted(DefaultAlert alert) {
      return mutedAlerts_.contains(alert.getTitle());
   }

   public void textUpdated(DefaultAlert alert) {
      studio_.events().post(new AlertUpdatedEvent(alert));
   }
   
   @Subscribe
   public void onShutdownCommencing(InternalShutdownCommencingEvent event) {
      if (!event.getIsCancelled()) {
         if (staticInstance_ != null) {
            staticInstance_.dispose();
         }
      }
   }
   
}
