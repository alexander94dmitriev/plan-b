// Copyright © 2018 Po Huit

// Plan B: EVE route planner with options

mod map;

fn main() {
    println!("{:?}", map::Map::fetch().unwrap());
}
