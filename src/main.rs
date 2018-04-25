// Copyright © 2018 Po Huit
// [This program is licensed under the "MIT License"]
// Please see the file LICENSE in the source
// distribution of this software for license terms.


// Plan B: EVE route planner with options

mod map;

fn main() {
    println!("{:?}", map::Map::fetch().unwrap());
}
