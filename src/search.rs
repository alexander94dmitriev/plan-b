// Copyright © 2018 Po Huit
// [This program is licensed under the "MIT License"]
// Please see the file LICENSE in the source
// distribution of this software for license terms.

pub use map::*;

pub fn search<'a>(_map: Map, src: &'a str, dest: &'a str) -> Option<Vec<&'a str>> {
    Some(vec![src, dest])
}
