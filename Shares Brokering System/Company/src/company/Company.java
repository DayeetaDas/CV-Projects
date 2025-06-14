//9"
//Code to create the json Array stored in json object with the details of the companies
package company;

/**
 *
 * @author dayee
 */

//importing all the header files
import java.io.FileWriter;
import java.io.IOException;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

//defining class
public class Company {

    //main function
    public static void main(String[] args) {
        
        // Putting all the details of the companies in diffreent json objects
        
// Company 1
        JSONObject companyDetails1 = new JSONObject();
        companyDetails1.put("companyName", "Apple Inc");
        companyDetails1.put("companySymbol", "AAPL");
        companyDetails1.put("number", 100);
        companyDetails1.put("currency", "USD");
        companyDetails1.put("price", 164.43);
        companyDetails1.put("date", "18/03/2022");
        
        
        
        //Company 2
        JSONObject companyDetails2 = new JSONObject();
        companyDetails2.put("companyName", "Microsoft Corporation");
        companyDetails2.put("companySymbol", "MSFT");
        companyDetails2.put("number", 149);
        companyDetails2.put("currency", "USD");
        companyDetails2.put("price", 300.43);
        companyDetails2.put("date", "17/03/2022");
        
        
        
        //Company 3
        JSONObject companyDetails3 = new JSONObject();
        companyDetails3.put("companyName", "Amazon.com");
        companyDetails3.put("companySymbol", "AMZN");
        companyDetails3.put("number", 104);
        companyDetails3.put("currency", "USD");
        companyDetails3.put("price", 3225.01);
        companyDetails3.put("date", "16/03/2022");
        
        
        
        //Company 4
        JSONObject companyDetails4 = new JSONObject();
        companyDetails4.put("companyName", "Tesla Inc");
        companyDetails4.put("companySymbol", "TSLA");
        companyDetails4.put("number", 111);
        companyDetails4.put("currency", "USD");
        companyDetails4.put("price", 905.39);
        companyDetails4.put("date", "15/03/2022");
        
        
        
        //Company 5
        JSONObject companyDetails5 = new JSONObject();
        companyDetails5.put("companyName", "Meta Platforms Inc");
        companyDetails5.put("companySymbol", "FB");
        companyDetails5.put("number", 120);
        companyDetails5.put("currency", "USD");
        companyDetails5.put("price", 216.49);
        companyDetails5.put("date", "19/03/2022");
        
        
        //Putting all the objeects in an array
        
        JSONArray companyList = new JSONArray();
        companyList.add(companyDetails1);
        companyList.add(companyDetails2);
        companyList.add(companyDetails3);
        companyList.add(companyDetails4);
        companyList.add(companyDetails5);
        
        //storing the json array in an json object named Company
        
        JSONObject companyObject = new JSONObject();
        companyObject.put("Company", companyList);
        
        //writing the json object in a .json file
        try (FileWriter file = new FileWriter("Company.json"))
        {
            file.write(companyObject.toJSONString());
            file.flush();
        }catch(IOException e)
        {
            e.printStackTrace();
        }
        
    }
    
}
