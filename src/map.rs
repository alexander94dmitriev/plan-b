// Copyright © 2018 Po Huit
// [This program is licensed under the "MIT License"]
// Please see the file LICENSE in the source
// distribution of this software for license terms.


// Map data management for Plan B

extern crate libflate;
use self::libflate::gzip;

extern crate serde_json;
use self::serde_json::Value;

use std::io::Error;
use std::collections::HashMap;
use std::fs::File;

#[derive(Clone, Copy, Debug, PartialEq, Eq, PartialOrd, Hash)]
pub struct SystemId(u32);

#[derive(Debug)]
pub struct SystemInfo {
    system_id: SystemId,
    name: String,
    stargates: Vec<SystemId>,
}

#[derive(Debug)]
pub struct Map(HashMap<SystemId, SystemInfo>);

impl Map {
    pub fn fetch() -> Result<Map, Error> {
        let map_file = File::open("eve-map.json.gz")?;
        let gunzip = gzip::Decoder::new(map_file)?;
        let map_data: Value = serde_json::from_reader(gunzip)?;
        let systems = map_data
            .get("systems")
            .expect("no systems")
            .as_object()
            .expect("bad systems");
        let mut map = HashMap::new();
        for (system_id_str, system) in systems {
            let system_id = SystemId(system_id_str.parse().unwrap());
            let name = system["name"].to_string();
            let stargates = Vec::new();
            let system_info = SystemInfo {
                system_id,
                name,
                stargates
            };
            map.insert(system_id, system_info);
        }
        Ok(Map(map))
    }
}
