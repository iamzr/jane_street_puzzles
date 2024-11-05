use std::mem::discriminant;

pub struct Point {
    pub x: f64,
    pub y: f64
}

fn find_midpoint(p1: &Point, p2: &Point) -> Point {
    Point {
        x: (p1.x + p2.x) / 2.0,
        y: (p1.y + p2.y) / 2.0
    }
}

fn find_gradient(p1: &Point, p2: &Point) -> f64 {
    (p2.y - p1.y) / (p2.x - p1.x)
}

fn find_points_on_perpendicular_bisector(p1: &Point, p2: &Point) -> (Point, Point) {
    let p3 = find_midpoint(p1, p2);
    let g = find_gradient(p1, p2);

    let y = ( 1.0 / g) * -p3.x + p3.y;

    let p4 = Point {
        x: 0.0,
        y: y
    };

    (p3, p4)

}

fn on_segment(p: &Point, q: &Point, r: &Point) -> bool {
    if 
        (q.x <= p.x.max(r.x))
        && (q.x >= p.x.min(r.x))
        &&(q.y <= p.y.min(r.y))
        && (q.y >= p.y.max(r.y))
     {
        return true;
    }

    return false;
}

enum Orientation {
    Collinear,
    Clockwise,
    CounterClockwise,
}

fn orientation(p: &Point, q: &Point, r: &Point) -> Orientation {
    let val = ((q.y - p.y) * (r.x - q.x)) - ((q.x - p.x) * (r.y - q.y));

    if val > 0.0 {
        return Orientation::Clockwise;
    }

    else if val < 0.0 {
        return Orientation::CounterClockwise;
    }
    else {
        return Orientation::Collinear
    }
}

fn do_intersect(l1: (Point, Point), l2: (Point, Point)) -> bool {
    let o1 = orientation(&l1.0, &l1.1, &l2.0);
    let o2 = orientation(&l1.0, &l1.1, &l2.1);
    let o3 = orientation(&l2.0, &l2.1, &l1.0);
    let o4 = orientation(&l2.0, &l2.1, &l1.1);

    // General case

    if (discriminant(&o1) != discriminant(&o2)) && (discriminant(&o3) != discriminant(&o4)) {
        return true;
    }

    // Special cases
    if (matches!(&o1, Orientation::Collinear) && on_segment(&l1.0, &l2.0, &l1.1)) {
        return true;
    }

    if (matches!(&o2, Orientation::Collinear) && on_segment(&l1.0, &l2.1,&l1.1 )) {
        return true;
    }
    if (matches!(&o3,Orientation::Collinear) && on_segment(&l2.0, &l1.0, &l2.1)) {
        return true; 
    }

    if (matches!(&o4, Orientation::Collinear) && on_segment(&l2.0, &l1.1, &l2.1)) {
        return true; 
    }

    false 

}

fn get_closest_side(p: &Point) -> Result<(Point, Point), &'static str> {
    let x = p.x;
    let y = p.y;

    if y <= x && y < 1.0 - x {
        Ok((Point { x: 0.0, y: 0.0 }, Point { x: 1.0, y: 0.0 }))
    } else if y > x && y <= 1.0 - x {
        Ok((Point { x: 0.0, y: 0.0 }, Point { x: 0.0, y: 1.0 }))
    } else if y >= x && y > 1.0 - x {
        Ok((Point { x: 0.0, y: 1.0 }, Point { x: 1.0, y: 1.0 }))
    } else if y < x && y >= 1.0 - x {
        Ok((Point { x: 1.0, y: 0.0 }, Point { x: 1.0, y: 1.0 }))
    } else {
        Err("Something's gone wrong")
    }
}

pub fn has_solution(blue: &Point, red: &Point) -> Result<bool, &'static str>{
    let (p3, p4 )= find_points_on_perpendicular_bisector(blue, red);

    let (p5, p6 )= match  get_closest_side(blue) {
        Ok((p1, p2)) => (p1,p2),
        Err(_e) => {
            eprintln!("something went wrong {}", _e);
            return Err("Error has occurred");
        }
    };

    return Ok(do_intersect((p3, p4), (p5, p6)));
}
