package com.forgelings.app;

import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.appwidget.AppWidgetManager;
import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Build;
import androidx.core.app.NotificationCompat;
import androidx.core.app.NotificationManagerCompat;
import com.getcapacitor.JSObject;
import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.CapacitorPlugin;

// Lets the web app feed the home-screen widget, and show a quiet countdown notification while a Forgeling wanders.
// The words arrive already in the player's language.
@CapacitorPlugin(name = "Widget")
public class WidgetBridgePlugin extends Plugin {
    static final String PREFS = "forgelings_widget";
    static final String CHANNEL = "forgelings_wander";
    static final int WANDER_ID = 7317;

    @PluginMethod
    public void update(PluginCall call) {
        Context ctx = getContext();
        SharedPreferences.Editor e = ctx.getSharedPreferences(PREFS, Context.MODE_PRIVATE).edit();
        e.putString("name", call.getString("name", ""));
        e.putString("line", call.getString("line", ""));
        e.putString("fresh", call.getString("fresh", ""));
        e.putString("wline", call.getString("wline", ""));
        e.putString("back", call.getString("back", ""));
        e.putString("day", call.getString("day", ""));
        e.putLong("until", call.getDouble("until", 0.0).longValue());
        String png = call.getString("png", null);
        if (png != null) e.putString("png", png);
        e.apply();
        ForgelingsWidgetProvider.refreshAll(ctx);
        JSObject r = new JSObject(); r.put("ok", true); call.resolve(r);
    }

    @PluginMethod
    public void wanderStart(PluginCall call) {
        Context ctx = getContext();
        long until = call.getDouble("until", 0.0).longValue();
        String title = call.getString("title", "");
        try {
            if (Build.VERSION.SDK_INT >= 26) {
                NotificationManager nm = (NotificationManager) ctx.getSystemService(Context.NOTIFICATION_SERVICE);
                if (nm != null && nm.getNotificationChannel(CHANNEL) == null) {
                    NotificationChannel ch = new NotificationChannel(CHANNEL, call.getString("channel", "Wandering"), NotificationManager.IMPORTANCE_LOW);
                    ch.setShowBadge(false);
                    nm.createNotificationChannel(ch);
                }
            }
            Intent open = ctx.getPackageManager().getLaunchIntentForPackage(ctx.getPackageName());
            PendingIntent pi = open == null ? null : PendingIntent.getActivity(ctx, 0, open, PendingIntent.FLAG_IMMUTABLE | PendingIntent.FLAG_UPDATE_CURRENT);
            NotificationCompat.Builder b = new NotificationCompat.Builder(ctx, CHANNEL)
                .setSmallIcon(R.drawable.ic_stat_forgelings)
                .setContentTitle(title)
                .setOngoing(true).setOnlyAlertOnce(true).setSilent(true)
                .setWhen(until).setShowWhen(true).setUsesChronometer(true)
                .setTimeoutAfter(Math.max(60_000L, until - System.currentTimeMillis() + 15 * 60_000L))
                .setCategory(NotificationCompat.CATEGORY_PROGRESS);
            if (Build.VERSION.SDK_INT >= 24) b.setChronometerCountDown(true);
            if (pi != null) b.setContentIntent(pi);
            NotificationManagerCompat.from(ctx).notify(WANDER_ID, b.build());
            JSObject r = new JSObject(); r.put("ok", true); call.resolve(r);
        } catch (SecurityException ex) {
            // notifications are off for Forgelings: the widget still counts down
            JSObject r = new JSObject(); r.put("ok", false); call.resolve(r);
        }
    }

    @PluginMethod
    public void wanderEnd(PluginCall call) {
        NotificationManagerCompat.from(getContext()).cancel(WANDER_ID);
        JSObject r = new JSObject(); r.put("ok", true); call.resolve(r);
    }
}
