// Copyright © 2018 Po Huit
// [This program is licensed under the "MIT License"]
// Please see the file LICENSE in the source
// distribution of this software for license terms.

extern crate min_max_heap;
use self::min_max_heap::MinMaxHeap;

use map::*;

use std::collections::HashMap;

pub fn search<'a>(
    map: &'a Map,
    src: &'a str,
    dest: &'a str,
    ) -> Option<Vec<SystemId>> {
    let start = map.by_name(src)?.system_id;
    let goal = map.by_name(dest)?.system_id;
    let mut q = MinMaxHeap::new();
    let mut closed: HashMap<SystemId, (usize, Option<SystemId>)> = HashMap::new();
    q.push((0, start, None));
    loop {
        let (dist, cur, parent) = q.pop_min()?;
        if cur == goal {
            let mut path = Vec::with_capacity(dist);
            path.push(cur);
            let mut next_stop = parent;
            while let Some(system_id) = next_stop {
                path.push(system_id);
                let (_, parent) = closed[&system_id];
                next_stop = parent;
            }
            path.reverse();
            return Some(path);
        }
        closed.insert(cur, (dist, parent));
        let map_info = map.by_system_id(cur);
        for child in map_info.stargates.iter() {
            if closed.contains_key(child) {
                continue;
            }
            q.push((dist + 1, *child, Some(cur)));
        }
    }
}
