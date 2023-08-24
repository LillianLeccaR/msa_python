# Libraries
from typing import List, Any
import pandas as pd
import requests
import sys
import os

# List of cities

cities_tot = ["Guilin,China",
              "Dissen,Germany",
              "Guatemala City,Guatemala",
              "Kandukur,India",
              "Nanaimo,British Columbia",
              "Uijeongbu-si,South Korea",
              "Yangon,Myanmar",
              "Jalpa de Mendez,Mexico",
              "Enugu,Nigeria",
              "Peterhead,Scotland",
              "Lima,Peru",
              "Singapore,Singapore",
              "Kaohsiung,Taiwan",
              "Grimesland,North Carolina",
              "Visalia,California",
              "Colonia del Sacramento,Uruguay"]


class WeatherForecast:
    """Class to get forecast data for the following dates using
        http://api.openweathermap.org/ data.
    """

    def __init__(
        self,
        api_key: str,
        ow_url: str = 'http://api.openweathermap.org/',
        geo_url: str = 'geo/1.0/direct?q={city}&limit=5&appid={api_key}',
        fct_url: str = 'data/2.5/forecast?lat={lat}&lon={lon}&units=metric&appid={api_key}',
    ) -> None:
        """Initializes the WeatherForecast class.

        Args:
            api_key (str): Key to use openweathermap enpoints.
                            Get one at https://openweathermap.org/api.
            ow_url (str, optional): Link to openweathermap data.
                                    Defaults to 'http://api.openweathermap.org/'.
            geo_url (str, optional):
                String with the additional link to use the geolocation endpoint.
                Defaults to 'geo/1.0/direct?q={city}&limit=5&appid={api_key}'.
            fct_url (str, optional):
                String with the additional link to use the forecast weather endpoint and
                get the weather prediction in degrees celsious.
                Defaults to 'data/2.5/forecast?lat={lat}&lon={lon}&units=metric&appid={api_key}'.
        """
        self.api_key = api_key
        self.url_geo_param = ow_url+geo_url
        self.url_fct_param = ow_url+fct_url

    @staticmethod
    def requests_val_json(url_path: str,
                          type_data: str,
                          ) -> Any:
        """Returns data from a given API endpoint and validate results.

        Args:
            url_path (str): Url endpoint.
            type_data (str):
                This method will make special validation when it ask the
                geolocation endpoint.

        Returns:
            Any: Data available in the requested endpoint.
        """
        resp = requests.get(url_path)
        if resp.status_code != 200:
            print(f'Error retrieving data for {type_data}: {resp.status_code}')
            sys.exit(1)
        if type_data == "city":
            if len(resp.json()) == 0:
                print(
                    f'Error locating city : {resp.status_code} (status code)')
                sys.exit(2)
            if type(resp.json()) != list:
                print(
                    f'Error, invalid data returned for city, {resp.status_code} (status code)')
                sys.exit(3)
        return resp

    @staticmethod
    def format_fct_weather(list_fct_weather: List,
                           city: str,) -> pd.DataFrame:
        """Method to format forecast data in a dataframe with the necessary data
            for the requested city.

        Args:
            list_fct_weather (List): Data object returned by the forecast endpoint.
            city (str): String with the city requested.

        Returns:
            pd.DataFrame:
                Dataframe with the necessary forecast data for the requested "city".
        """
        df_fct_weather = pd.json_normalize(list_fct_weather)
        df_fct_weather['city'] = city
        df_fct_weather['dt_txt'] = pd.to_datetime(
            df_fct_weather['dt_txt'], format='%Y-%m-%d %H:%M:%S')
        df_fct_weather['date'] = df_fct_weather['dt_txt'].dt.date
        df_fct_weather = df_fct_weather[[
            'city', 'date', 'dt_txt', 'main.temp_min', 'main.temp_max']]

        return df_fct_weather

    def get_data_cities(self,
                        cities: List,
                        ) -> pd.DataFrame:
        """Extracts data from the Open weather map and format it in dataframe
           for an specific list of cities.

        Args:
            cities (List): List of cities to ask in open weather API.

        Returns:
            pd.DataFrame: Dataframe with the necesary data for the list of "cities".
        """
        data_tot_cities = pd.DataFrame()

        for city in cities:
            print("City : " + city)
            url_geo_param = self.url_geo_param.format(city=city,
                                                      api_key=self.api_key)

            lat_lon_resp = self.requests_val_json(
                url_path=url_geo_param, type_data='city')
            data_lat_lon = lat_lon_resp.json()

            print(f"{city} : "+str(len(pd.DataFrame(data_lat_lon))) + " cities")
            print(pd.DataFrame(data_lat_lon))
            # we will use the values for the first city
            data_lat_lon = data_lat_lon[0]
            url_fct_param = self.url_fct_param.format(
                lat=data_lat_lon['lat'], lon=data_lat_lon['lon'], api_key=self.api_key)

            df_fct_weather = self.requests_val_json(
                url_path=url_fct_param, type_data='fct').json()
            df_fct_weather = self.format_fct_weather(df_fct_weather['list'],
                                                     city)
            data_tot_cities = pd.concat([data_tot_cities, df_fct_weather])
            os.system("cls")
        return data_tot_cities

    def generate_summary_fct(self,
                             cities: List,
                             ) -> pd.DataFrame:
        """Generates a with the weather forecast summary for a list of "cities" in the requested format.

        Args:
            cities (List): List of cities to ask in open weather API.

        Returns:
            pd.DataFrame: weather forecast summary for a list of "cities.
        """
        cities = list(dict.fromkeys(cities))
        data_city = self.get_data_cities(cities)
        # Agreggate by city-date
        data_summary = data_city\
            .groupby(["city", "date"]).agg(
                Count=pd.NamedAgg(column="main.temp_min", aggfunc="count"),
                Min=pd.NamedAgg(column="main.temp_min", aggfunc="min"),
                Max=pd.NamedAgg(column="main.temp_max", aggfunc="max")).reset_index()
        # Filter only the nex 4 days ( starting wiith the first day with predictions for 8 blocks )
        data_summary = data_summary[data_summary.Count == 8]
        # rank dates
        data_summary['date_rank'] = data_summary.groupby(
            'city')['date'].rank(method='first').astype('int')
        data_summary = data_summary[(data_summary.date_rank <= 4)]
        data_summary['date_rank'] = data_summary['date_rank'].astype(str)

        # Convert rows to columns
        data_summary = data_summary.pivot(
            index=['city'], columns='date_rank', values=['Min', 'Max'])
        data_summary.columns = [" ".join((i, j))
                                for i, j in data_summary.columns]
        data_summary = data_summary.reset_index()

        # Calculate metrics by rows
        data_summary["Min Avg"] = data_summary.loc[:, [
            "Min 1", "Min 2", "Min 3", "Min 4"]].mean(axis=1)
        data_summary["Max Avg"] = data_summary.loc[:, [
            "Max 1", "Max 2", "Max 3", "Max 4"]].mean(axis=1)
        data_summary = data_summary[["city", "Min 1", "Max 1", "Min 2",
                                     "Max 2", "Min 3", "Max 3", "Min 4",
                                     "Max 4", "Min Avg", "Max Avg"]]
        # Format names and decimals
        data_summary = data_summary.rename(columns={"city": "City"})
        data_summary['City'] = data_summary['City'].str.replace(",", ", ")

        cols_to_string = list(data_summary.columns[1:])
        data_summary[cols_to_string] = data_summary[cols_to_string].applymap(
            lambda x: '{0:.2f}'.format(x))

        # Rank cities
        cities_mod = [x.replace(",", ", ") for x in cities]
        data_summary = data_summary.iloc[sorted(range(
            len(data_summary)), key=lambda x: cities_mod.index(data_summary['City'][x]))]

        return data_summary


# Ussage
get_weather_forecast = WeatherForecast(
    api_key='8efa2a45d2cb7a48634f085a2de091bd')
summary_data_city = get_weather_forecast.generate_summary_fct(
    cities=cities_tot)

print(summary_data_city.head(30))
summary_data_city.to_csv('temp.csv', index=False, sep=",")
