//9"
// Code to create web services for listing all the company details
package listDetails;

import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.Iterator;
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
@Path("listDetails")
public class ListDetails {

    @Context
    private UriInfo context;

    /**
     * Creates a new instance of ListDetails
     */
    public ListDetails() {
    }

    /**
     * Retrieves representation of an instance of listDetails.ListDetails
     * @return an instance of java.lang.String
     */
    @GET
    @Produces(MediaType.TEXT_PLAIN)
    public String getText(){
        //TODO return proper representation object
        JSONParser parser = new JSONParser();
        StringBuilder str = new StringBuilder();
        
        try
        {
            JSONObject jsonObject = (JSONObject) parser.parse(new FileReader("C:/Users/dayee/Documents/SCCCN0830182/Company/Company.json"));

            JSONArray companies = (JSONArray)jsonObject.get("Company");
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
                String date = (String)company.get("date");
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
}
