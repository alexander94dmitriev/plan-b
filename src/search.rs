// Copyright © 2018 Po Huit
// [This program is licensed under the "MIT License"]
// Please see the file LICENSE in the source
// distribution of this software for license terms.

use map::*;

pub fn search<'a>(
    map: &'a Map,
    src: &'a str,
    dest: &'a str,
) -> Option<Vec<SystemId>> {
    Some(vec![map.by_name(src)?.system_id, map.by_name(dest)?.system_id])
}
