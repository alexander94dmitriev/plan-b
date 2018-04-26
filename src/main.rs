// Copyright © 2018 Po Huit
// [This program is licensed under the "MIT License"]
// Please see the file LICENSE in the source
// distribution of this software for license terms.

// Plan B: EVE route planner with options

mod map;
mod search;

pub use map::*;
pub use search::*;

fn main() {
    let mut args = std::env::args();
    let src = (&mut args).skip(1).next().expect("no source");
    let dest = (&mut args).next().expect("no destination");
    let map = Map::fetch().expect("could not open map");
    let path = search(&map, &src, &dest).expect("no route");
    for system_id in path {
        let system = map.by_system_id(system_id).unwrap();
        println!("{:?}", system);
    }
}
