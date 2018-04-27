// Copyright © 2018 Po Huit
// [This program is licensed under the "MIT License"]
// Please see the file LICENSE in the source
// distribution of this software for license terms.

extern crate min_max_heap;
use self::min_max_heap::MinMaxHeap;

use map::*;

use std::collections::HashMap;

pub fn shortest_route<'a>(
    map: &'a Map,
    start: SystemId,
    goal: SystemId,
    ) -> Option<Vec<SystemId>> {
    let mut q = MinMaxHeap::new();
    let mut closed: HashMap<SystemId, (usize, Option<SystemId>)>
        = HashMap::new();
    q.push((0, start, None));
    loop {
        let (dist, cur, parent) = q.pop_min()?;
        if closed.contains_key(&cur) {
            continue;
        }
        closed.insert(cur, (dist, parent));
        if cur == goal {
            let mut route = Vec::with_capacity(dist);
            route.push(cur);
            let mut next_stop = parent;
            while let Some(system_id) = next_stop {
                route.push(system_id);
                let (_, parent) = closed[&system_id];
                next_stop = parent;
            }
            route.reverse();
            return Some(route);
        }
        let map_info = map.by_system_id(cur);
        for child in map_info.stargates.iter() {
            q.push((dist + 1, *child, Some(cur)));
        }
    }
}
