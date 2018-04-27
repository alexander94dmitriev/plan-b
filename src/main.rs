// Copyright © 2018 Po Huit
// [This program is licensed under the "MIT License"]
// Please see the file LICENSE in the source
// distribution of this software for license terms.

// Plan B: EVE route planner with options

mod map;
mod search;

pub use map::*;
pub use search::*;

fn find_system(map: &Map, name: &str) -> SystemId {
    map.by_name(name)
        .expect(&format!("could not find {} in map", name))
        .system_id
}

fn main() {
    let mut args = std::env::args();
    let start = (&mut args).skip(1).next().expect("no source");
    let goal = (&mut args).next().expect("no destination");
    let map = Map::fetch().expect("could not open map");
    let start_id = find_system(&map, &start);
    let goal_id = find_system(&map, &goal);
    let path = shortest_path(&map, start_id, goal_id)
        .expect(&format!("no route found from {} to {}", start, goal));
    for system_id in path {
        let system = map.by_system_id(system_id);
        println!("{}", system.name);
    }
}
