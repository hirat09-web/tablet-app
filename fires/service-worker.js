const CACHE_NAME = 'ceforaa-map-v2';

const FILES_TO_CACHE = [

  './',
  './index.html',

  './leaflet.css',
  './leaflet.js',

  './logo.png',

  './Huanipaca_firerisk.png',
  './Huanipaca_water.png',
  './Huanipaca_degradation.png',
  './Huanipaca_landuse.png',
  './Huanipaca.geojson',
  './Huanipaca_labels.geojson',

  './Yanatile_firerisk.png',
  './Yanatile_water.png',
  './Yanatile_degradation.png',
  './Yanatile_landuse.png',
  './Yanatile.geojson',
  './Yanatile_labels.geojson',

  './SJO_firerisk.png',
  './SJO_water.png',
  './SJO_degradation.png',
  './SJO_landuse.png',
  './SJO.geojson',
  './SJO_labels.geojson',

  './fires/Huanipaca_fire_2017.geojson',
  './fires/Huanipaca_fire_2018.geojson',
  './fires/Huanipaca_fire_2019.geojson',
  './fires/Huanipaca_fire_2020.geojson',
  './fires/Huanipaca_fire_2021.geojson',
  './fires/Huanipaca_fire_2022.geojson',
  './fires/Huanipaca_fire_2023.geojson',
  './fires/Huanipaca_fire_2024.geojson',
  './fires/Huanipaca_fire_2025.geojson',

  './fires/Yanatile_fire_2017.geojson',
  './fires/Yanatile_fire_2018.geojson',
  './fires/Yanatile_fire_2019.geojson',
  './fires/Yanatile_fire_2020.geojson',
  './fires/Yanatile_fire_2021.geojson',
  './fires/Yanatile_fire_2022.geojson',
  './fires/Yanatile_fire_2023.geojson',
  './fires/Yanatile_fire_2024.geojson',
  './fires/Yanatile_fire_2025.geojson',

  './fires/SJO_fire_2017.geojson',
  './fires/SJO_fire_2018.geojson',
  './fires/SJO_fire_2019.geojson',
  './fires/SJO_fire_2020.geojson',
  './fires/SJO_fire_2021.geojson',
  './fires/SJO_fire_2022.geojson',
  './fires/SJO_fire_2023.geojson',
  './fires/SJO_fire_2024.geojson',
  './fires/SJO_fire_2025.geojson'

];

self.addEventListener('install', function(event){

  event.waitUntil(

    caches.open(CACHE_NAME)
      .then(function(cache){

        return cache.addAll(FILES_TO_CACHE);

      })

  );

});

self.addEventListener('activate', function(event){

  event.waitUntil(

    caches.keys()
      .then(function(keys){

        return Promise.all(

          keys.map(function(key){

            if(key !== CACHE_NAME){

              return caches.delete(key);

            }

          })

        );

      })

  );

});

self.addEventListener('fetch', function(event){

  event.respondWith(

    caches.match(event.request)
      .then(function(response){

        return response || fetch(event.request);

      })

  );

});