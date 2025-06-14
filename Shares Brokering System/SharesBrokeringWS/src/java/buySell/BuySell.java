//9"
// Code to create web services for buying and selling shares
package buySell;

import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import javax.ws.rs.core.Context;
import javax.ws.rs.core.UriInfo;
import javax.ws.rs.Consumes;
import javax.ws.rs.Produces;
import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.PUT;
import javax.ws.rs.QueryParam;
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
@Path("buySell")
public class BuySell {

    @Context
    private UriInfo context;

    /**
     * Creates a new instance of BuySell
     */
    public BuySell() {
    }

    /**
     * Retrieves representation of an instance of buySell.BuySell
     * @return an instance of java.lang.String
     */
    @GET
    @Produces(MediaType.TEXT_PLAIN)
    public String getText(@QueryParam("fromCmp")String fromCmp, 
                           @QueryParam("toCmp")String toCmp,
                           @QueryParam("Buy")Long buy,
                           @QueryParam("Sell")Long sell) {
        //TODO return proper representation object
        
        
        JSONParser parser = new JSONParser();
        StringBuilder str = new StringBuilder();
        
        try
        {
            JSONObject jsonObject = (JSONObject) parser.parse(new FileReader("C:/Users/dayee/Documents/SCCCN0830182/Company/Company.json"));

            JSONArray companies = (JSONArray)jsonObject.get("Company");
            double mc = 0.0;
            
            //JSONArray companies = (JSONArray)jsonObject.get("Company");
            //Iterator iterator = companies.iterator();
            //while (iterator.hasNext()) 
            for(Object o : companies)
            {
                JSONObject company = (JSONObject) o;
                String name = (String)company.get("companyName");
                str.append(name + "\n");
                String symbol = (String)company.get("companySymbol");
                str.append(symbol + "\n");
                Long number = (Long)company.get("number");
                str.append(number + "\n");
                String currency = (String)company.get("currency");
                str.append(currency + "\n");
                Double price = (Double)company.get("price");
                str.append(price + "\n");
                mc = price * number;
                str.append("Market capitalization is: " + mc + "\n");
                String date = (String)company.get("date");
                str.append(date + "\n");
                
            }
            
            str.append("===================================================\n");
            str.append("The new details are:\n");
            str.append("===================================================\n");
            
            for(Object o : companies)
            {
                JSONObject company = (JSONObject) o;
                String name = (String)company.get("companyName");
                
                String symbol = (String)company.get("companySymbol");
               
                Long number = (Long)company.get("number");
               
                String currency = (String)company.get("currency");
                
                Double price = (Double)company.get("price");
                
                String date = (String)company.get("date");
                
                if(symbol.equals(fromCmp))
                {
                    number = number - buy;
                    mc = price * number;
                }
                
                if(symbol.equals(toCmp))
                {
                    number = number + sell;
                }
                
                str.append(name + "\n");
                str.append(symbol + "\n");
                str.append(number + "\n");
                str.append(currency + "\n");
                str.append(price + "\n");
                str.append("Current market capitalization is: " + mc + "\n");
                str.append(date + "\n");
                
            }
        }catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } catch (ParseException e) {
            e.printStackTrace();
        }
        
        return str.toString();
    
    }

    /**
     * PUT method for updating or creating an instance of BuySell
     * @param content representation for the resource
     */
    
}
