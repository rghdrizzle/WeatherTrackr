package main

import(
	"net/http"
	"strings"
	"encoding/json"
	"io/ioutil"


)

type apiConfigData struct{
	OpenWeatherMapApiKey string `json:"OpenWeatherMapApiKey"`

}
type weatherData struct{
	Name string `json:"name"`
	Main struct{
		Kelvin float64 `json:"temp"`
	}`json:"main"`
	Weather[] struct {
		Main string `json:"main"`
		Description string `json:"description"`

	}`jason:"weather"`
}


func loadApiConfig(filename string)(apiConfigData,error){
	bytes, err := ioutil.ReadFile(filename)


	if err!=nil{
		return apiConfigData{}, err
	}

	var c apiConfigData 
	err = json.Unmarshal(bytes,&c)
	if err!=nil{
		return apiConfigData{} , err
	}
	return c , nil
}
func hello(w http.ResponseWriter, r *http.Request){
	enableCors(&w)
	w.Write([]byte("Hello from rghdrizzle \n"))
}

func query(city string) ( weatherData,error){
	apiConfig , err := loadApiConfig(".apiconfig")

	if err!=nil{
		return weatherData{}, err
	}
	resp, err := http.Get("http://api.openweathermap.org/data/2.5/weather?APPID="+apiConfig.OpenWeatherMapApiKey+"&q="+city)
	if err!=nil{
		return weatherData{}, err
	}
	defer resp.Body.Close()

	var d weatherData
	if err:= json.NewDecoder(resp.Body).Decode(&d); err!=nil{
		return weatherData{}, err
	}
	return d , nil
}

func main(){
	http.HandleFunc("/",hello)
	http.HandleFunc("/weather/",func(w  http.ResponseWriter , r *http.Request){
		enableCors(&w)
		city:= strings.SplitN(r.URL.Path,"/",3)[2]
		data,err:=query(city)
		if err!=nil{
			http.Error(w , err.Error(), http.StatusInternalServerError)
			return
		}
		w.Header().Set("Content-Type","application/json; charset=utf-8")
		json.NewEncoder(w).Encode(data)
	})

	http.ListenAndServe(":8080",nil)
}
func enableCors(w *http.ResponseWriter) {
	(*w).Header().Set("Access-Control-Allow-Origin", "*")
	}