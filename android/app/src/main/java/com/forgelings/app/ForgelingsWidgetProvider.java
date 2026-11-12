package com.forgelings.app;

import android.app.PendingIntent;
import android.appwidget.AppWidgetManager;
import android.appwidget.AppWidgetProvider;
import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.SystemClock;
import android.util.Base64;
import android.view.View;
import android.widget.RemoteViews;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

// The home-screen widget: your Forgeling, its name, and today's card or the wandering countdown.
public class ForgelingsWidgetProvider extends AppWidgetProvider {

    static void refreshAll(Context ctx) {
        AppWidgetManager m = AppWidgetManager.getInstance(ctx);
        int[] ids = m.getAppWidgetIds(new ComponentName(ctx, ForgelingsWidgetProvider.class));
        for (int id : ids) m.updateAppWidget(id, views(ctx));
    }

    @Override
    public void onUpdate(Context ctx, AppWidgetManager m, int[] ids) {
        for (int id : ids) m.updateAppWidget(id, views(ctx));
    }

    static RemoteViews views(Context ctx) {
        SharedPreferences p = ctx.getSharedPreferences(WidgetBridgePlugin.PREFS, Context.MODE_PRIVATE);
        RemoteViews v = new RemoteViews(ctx.getPackageName(), R.layout.forgelings_widget);
        String name = p.getString("name", "");
        v.setTextViewText(R.id.fw_name, name.isEmpty() ? "Forgelings" : name);
        long until = p.getLong("until", 0L), now = System.currentTimeMillis();
        String today = new SimpleDateFormat("yyyy-MM-dd", Locale.US).format(new Date());
        String day = p.getString("day", ""), line = p.getString("line", ""), fresh = p.getString("fresh", "");
        if (!day.isEmpty() && !day.equals(today) && !fresh.isEmpty()) line = fresh;
        if (until > now) {
            v.setTextViewText(R.id.fw_line, p.getString("wline", ""));
            v.setViewVisibility(R.id.fw_timer, View.VISIBLE);
            v.setChronometer(R.id.fw_timer, SystemClock.elapsedRealtime() + (until - now), null, true);
            v.setChronometerCountDown(R.id.fw_timer, true);
        } else {
            String back = p.getString("back", "");
            v.setTextViewText(R.id.fw_line, until > 0 && !back.isEmpty() ? back : line);
            v.setViewVisibility(R.id.fw_timer, View.GONE);
        }
        String png = p.getString("png", null);
        if (png != null) {
            try {
                byte[] b = Base64.decode(png, Base64.DEFAULT);
                Bitmap bm = BitmapFactory.decodeByteArray(b, 0, b.length);
                if (bm != null) v.setImageViewBitmap(R.id.fw_sprite, Bitmap.createScaledBitmap(bm, bm.getWidth() * 4, bm.getHeight() * 4, false));
            } catch (IllegalArgumentException ignored) {}
        }
        Intent open = ctx.getPackageManager().getLaunchIntentForPackage(ctx.getPackageName());
        if (open != null) v.setOnClickPendingIntent(R.id.fw_root, PendingIntent.getActivity(ctx, 1, open, PendingIntent.FLAG_IMMUTABLE | PendingIntent.FLAG_UPDATE_CURRENT));
        return v;
    }
}
