//9"
// Code to create web services for getting company details in json format
package returnJson;

import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import javax.ws.rs.core.Context;
import javax.ws.rs.core.UriInfo;
import javax.ws.rs.Consumes;
import javax.ws.rs.Produces;
import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.PUT;
import javax.ws.rs.core.MediaType;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;
import java.util.*;
/**
 * REST Web Service
 *
 * @author dayee
 */
@Path("returnJson")
public class ReturnJson {

    @Context
    private UriInfo context;

    /**
     * Creates a new instance of ReturnJson
     */
    public ReturnJson() {
    }

    /**
     * Retrieves representation of an instance of returnJson.ReturnJson
     * @return an instance of java.lang.String
     */
    @GET
    @Produces(MediaType.APPLICATION_JSON)
    public String getJson() {
        //TODO return proper representation object
        JSONParser parser = new JSONParser();
        JSONArray companyList = new JSONArray();
        
        try
        {
            JSONObject jsonObject = (JSONObject) parser.parse(new FileReader("C:/Users/dayee/Documents/SCCCN0830182/Company/Company.json"));

            JSONArray companies = (JSONArray)jsonObject.get("Company");
            
            JSONObject companyDetails1 = new JSONObject();
            JSONObject companyDetails2 = new JSONObject();
            JSONObject companyDetails3 = new JSONObject();
            JSONObject companyDetails4 = new JSONObject();
            JSONObject companyDetails5 = new JSONObject();
            
            
            for(Object o : companies)
            {
                JSONObject company = (JSONObject) o;
                String name = (String)company.get("companyName");
                String symbol = (String)company.get("companySymbol");
                Long number = (Long)company.get("number");
                String currency = (String)company.get("currency");
                Double price = (Double)company.get("price");
                String date = (String)company.get("date");
                
                if(symbol.equals("AAPL"))
                {
                    companyDetails1.put("companyName", name);
                    companyDetails1.put("companySymbol", symbol);
                    companyDetails1.put("number", number);
                    companyDetails1.put("currency", currency);
                    companyDetails1.put("price", price);
                    companyDetails1.put("date", date);
                }
                
                else if(symbol.equals("MSFT"))
                {
                    companyDetails2.put("companyName", name);
                    companyDetails2.put("companySymbol", symbol);
                    companyDetails2.put("number", number);
                    companyDetails2.put("currency", currency);
                    companyDetails2.put("price", price);
                    companyDetails2.put("date", date);
                }
                
                else if(symbol.equals("AMZN"))
                {
                    companyDetails3.put("companyName", name);
                    companyDetails3.put("companySymbol", symbol);
                    companyDetails3.put("number", number);
                    companyDetails3.put("currency", currency);
                    companyDetails3.put("price", price);
                    companyDetails3.put("date", date);
                }
                
                else if(symbol.equals("TSLA"))
                {
                    companyDetails4.put("companyName", name);
                    companyDetails4.put("companySymbol", symbol);
                    companyDetails4.put("number", number);
                    companyDetails4.put("currency", currency);
                    companyDetails4.put("price", price);
                    companyDetails4.put("date", date);
                }
                
                else if(symbol.equals("FB"))
                {
                    companyDetails5.put("companyName", name);
                    companyDetails5.put("companySymbol", symbol);
                    companyDetails5.put("number", number);
                    companyDetails5.put("currency", currency);
                    companyDetails5.put("price", price);
                    companyDetails5.put("date", date);
                }
                
            }
            
            companyList.add(companyDetails1);
            companyList.add(companyDetails2);
            companyList.add(companyDetails3);
            companyList.add(companyDetails4);
            companyList.add(companyDetails5);
            
            /*
            FileWriter file = new FileWriter("Read.json");
            file.write(companyObject.toJSONString());
            file.flush();
            */
            
        }catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } catch (ParseException e) {
            e.printStackTrace();
        }
        JSONObject companyObject = new JSONObject();
        companyObject.put("Company", companyList);
        
        return companyObject.toString();
    }

}
