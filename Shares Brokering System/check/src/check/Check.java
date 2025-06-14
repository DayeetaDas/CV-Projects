/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package check;

/**
 *
 * @author dayee
 */
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.Iterator;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;
import java.util.*;

public class Check {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        // TODO code application logic here
        
        JSONParser parser = new JSONParser();
        StringBuilder str = new StringBuilder();
        
        try
        {
            JSONObject jsonObject = (JSONObject) parser.parse(new FileReader("C:/Users/dayee/Documents/SCCCN0830182/Company/Company.json"));

            JSONArray companies = (JSONArray)jsonObject.get("Company");
            
            Scanner sc = new Scanner(System.in);
            String fromCmp = "", toCmp = "";Long buy, sell;
            System.out.println("Please enter the company code from which you want to buy:");
            fromCmp = sc.nextLine();
            System.out.println("Please enter the company code to which you want to sell:");
            toCmp = sc.nextLine();
            System.out.println("Please enter how much u want to buy:");
            buy = sc.nextLong();
            System.out.println("Please enter how much you want to sell:");
            sell = sc.nextLong();
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
            
            System.out.println(str.toString());
            
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
                str.append(date + "\n");
                
            }
        }catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } catch (ParseException e) {
            e.printStackTrace();
        }
        
        System.out.println(str.toString());
    }
    
}
