/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package myRS;

import javax.ws.rs.Consumes;
import javax.ws.rs.Produces;
import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.PUT;
import org.json.JSONArray;
import org.json.JSONObject;

/**
 * REST Web Service
 *
 * @author taha-m
 */
@Path("curCodes")
public class CurCodesRS {

    /**
     * Creates a new instance of CurConvRS @Path("/{a:path1|path2}")
     */
    public CurCodesRS() {
    }

    /**
     * Retrieves representation of an instance of myRS.CurConvRS
     * @return an instance of java.lang.String
     */
    @GET
    @Produces("application/json")
    public String getJson() {

        JSONArray ja = new JSONArray();

        for (ExRate exr : ExRate.values()) {
            JSONObject job = new JSONObject();
            job.put("name", exr.curName());
            job.put("code", exr.name());
            job.put("rate", exr.rateInGBP());
            ja.put(job);
        }

        JSONObject rootJobj = new JSONObject();
        
        rootJobj.put("CurrConv", ja);
        
        return rootJobj.toString();
    }
    //
    @PUT
    @Consumes("application/json")
    public void putJson(String content) {
    }
    
 
    public enum ExRate {
        AED ("UAE Dirham", 0.203),
        ARS ("Argentine Peso", 0.007),
        AUD ("Australian Dollar", 0.526),
        BGN ("Bulgarian Lev", 0.426),
        BRL ("Brazilian Real", 0.138),
        BWP ("Botswana Pula", 0.065),
        CAD ("Canadian Dollar", 0.588),
        CHF ("Swiss Franc", 0.802),
        CLP ("Chilean Peso", 0.0009),
        CNY ("Chinese Yuan", 0.117),
        COP ("Colombian Peso", 0.0002),
        CUP ("Cuban Peso", 0.031),        
        DKK ("Danish Krone", 0.112),
        EGP ("Egypt Pounds", 0.047),
        EUR ("Euro", 0.83),
        GBP ("British pound", 1.0),
        HKD ("Hong Kong Dollar", 0.096),
        HRK ("Croatian Kuna", 0.11),
        HUF ("Hungarian Forint", 0.002),
        ILS ("Israeli Shekel", 0.234),
        INR ("Indian Rupee", 0.001),
        ISK ("Iceland Krona", 0.006),
        JPY ("Japanese Yen", 0.006),
        KRW ("South Korean Won", 0.0006),
        KZT ("Kazakhstani Tenge", 0.002),
        LKR ("Sri Lanka Rupee", 0.004),
        LYD ("Libyan Dinar", 0.163),
        MXN ("Mexican Peso", 0.036),
        MYR ("Malaysian Ringgit", 0.178),
        NOK ("Norwegian Kroner", 0.083),
        NPR ("Nepalese Rupee", 0.006),
        NZD ("New Zealand Dollar", 0.0492),
        OMR ("Omani Rial", 1.941),
        PKR ("Pakistan Rupee", 0.004),
        QAR ("Qatari Rial", 0.21),
        RON ("Romanian Leu", 0.168),
        RUB ("Russian Ruble", 0.001),
        SAR ("Saudi Riyal", 0.2),
        SDG ("Sudanese Pound",0.002),
        SEK ("Swedish Krona", 0.08),
        SGD ("Singapore Dollar", 0.55),
        THB ("Thai Baht", 0.022),
        TRY ("Turkish Lira", 0.055),
        TTD ("Trinidad/Tobago Dollar", 0.11),
        TWD ("Taiwan Dollar", 0.027),
        UAH ("Ukrainian hryvnia", 0.026),
        USD ("United States Dollar", 0.746),
        VEF ("Venezuelan Bolivar", 0.000002),
        ZAR ("South African Rand", 0.048);

        private final double rateInGBP;
        private final String curName;
        ExRate(String curName,double rateInGBP) {
            this.rateInGBP = rateInGBP;
            this.curName = curName;
        }
        double rateInGBP()   { return rateInGBP; }
        String curName()   { return curName; }
    }
}
