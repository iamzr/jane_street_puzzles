use std::mem::discriminant;
use std::f64::INFINITY;

#[derive(Debug, PartialEq)]
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

fn find_points_on_perpendicular_bisector(p1: &Point, p2: &Point) -> Result<(Point, Point), &'static str> {
    if p1 == p2 {
        return Err("Identical points do not define a line")
    }

    let p3 = find_midpoint(p1, p2);
    let g = find_gradient(p1, p2);

    // Vertical line
    if g == INFINITY {
        let p4 = Point { x: 0.0 , y: p3.y };

        return Ok((p3, p4))
    }

    // Horizontal line
    if g == 0.0 {
        let p4 = Point { x: p3.x, y: 0.0};

        return Ok((p3,  p4))
    }


    let y = -( 1.0 / g) * -p3.x + p3.y;

    let p4 = Point {
        x: 0.0,
        y: y
    };

    Ok((p3, p4))

}

fn on_segment(p: &Point, q: &Point, r: &Point) -> bool {
    if 
        (q.x <= p.x.max(r.x))
        && (q.x >= p.x.min(r.x))
        &&(q.y >= p.y.min(r.y))
        && (q.y <= p.y.max(r.y))
     {
        return true;
    }

    return false;
}

#[derive(Debug, PartialEq)]
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

fn do_intersect(l1: &(Point, Point), l2: &(Point, Point)) -> bool {
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
    } else if x == 0.5 && y == 0.5 {
        Ok((Point { x: 0.0, y: 0.0 }, Point { x: 1.0, y: 0.0 }))
    } else {
        Err("Something's gone wrong")
    }
}

pub fn has_solution(blue: &Point, red: &Point) -> Result<bool, &'static str>{
    let (p3, p4 )= match find_points_on_perpendicular_bisector(blue, red) {
        Ok((p3, p4)) => (p3, p4),
        Err(_e) =>  {
            eprintln!("something went wrong {}", _e);
            return Err(_e);
        }
    };

    let (p5, p6 )= match  get_closest_side(blue) {
        Ok((p1, p2)) => (p1,p2),
        Err(_e) => {
            eprintln!("something went wrong {}", _e);
            return Err(_e);
        }
    };

    return Ok(do_intersect(&(p3, p4), &(p5, p6)));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_get_closest_side_bottom_edge() {
        let p = Point { x: 0.2, y: 0.1 };
        let expected = Ok((
            Point { x: 0.0, y: 0.0 },
            Point { x: 1.0, y: 0.0 },
        ));
        assert_eq!(get_closest_side(&p), expected);
    }

    #[test]
    fn test_get_closest_side_left_edge() {
        let p = Point { x: 0.1, y: 0.2 };
        let expected = Ok((
            Point { x: 0.0, y: 0.0 },
            Point { x: 0.0, y: 1.0 },
        ));
        assert_eq!(get_closest_side(&p), expected);
    }

    #[test]
    fn test_get_closest_side_top_edge() {
        let p = Point { x: 0.2, y: 0.9 };
        let expected = Ok((
            Point { x: 0.0, y: 1.0 },
            Point { x: 1.0, y: 1.0 },
        ));
        assert_eq!(get_closest_side(&p), expected);
    }

    #[test]
    fn test_get_closest_side_right_edge() {
        let p = Point { x: 0.9, y: 0.2 };
        let expected = Ok((
            Point { x: 1.0, y: 0.0 },
            Point { x: 1.0, y: 1.0 },
        ));
        assert_eq!(get_closest_side(&p), expected);
    }

    #[test]
    fn test_get_closest_side_bottom_left_corner() {
        let p = Point { x: 0.0, y: 0.0 };
        let expected = Ok((
            Point { x: 0.0, y: 0.0 },
            Point { x: 1.0, y: 0.0 },
        ));
        assert_eq!(get_closest_side(&p), expected);
    }

    #[test]
    fn test_get_closest_side_top_right_corner() {
        let p = Point { x: 1.0, y: 1.0 };
        let expected = Ok((
            Point { x: 0.0, y: 1.0 },
            Point { x: 1.0, y: 1.0 },
        ));
        assert_eq!(get_closest_side(&p), expected);
    }

    #[test]
    fn test_get_closest_side_to_middle() {
        let p = Point { x: 0.5, y: 0.5 };
        let expected = Ok((
            Point { x: 0.0, y: 0.0 },
            Point { x: 1.0, y: 0.0 },
        ));
        assert_eq!(get_closest_side(&p), expected);
    }

    #[test]
    fn test_on_segment() {
        // Point lies on the segment
        let p = Point { x: 1.0, y: 1.0 };
        let q = Point { x: 2.0, y: 2.0 };
        let r = Point { x: 3.0, y: 3.0 };
        assert!(on_segment(&p, &q, &r));

        // Point does not lie on the segment
        let q = Point { x: 4.0, y: 4.0 };
        assert!(!on_segment(&p, &q, &r));
    }

    #[test]
    fn test_orientation() {
        let p = Point { x: 0.0, y: 0.0 };
        let q = Point { x: 4.0, y: 4.0 };
        let r = Point { x: 1.0, y: 2.0 };

        // CounterClockwise
        assert_eq!(orientation(&p, &q, &r), Orientation::CounterClockwise);

        // Clockwise
        let r = Point { x: 2.0, y: 1.0 };
        assert_eq!(orientation(&p, &q, &r), Orientation::Clockwise);

        // Collinear
        let r = Point { x: 2.0, y: 2.0 };
        assert_eq!(orientation(&p, &q, &r), Orientation::Collinear);
    }

    #[test]
    fn test_do_intersect() {
        let l1 = (
            Point { x: 1.0, y: 1.0 },
            Point { x: 4.0, y: 4.0 },
        );
        let l2 = (
            Point { x: 1.0, y: 4.0 },
            Point { x: 4.0, y: 1.0 },
        );

        // Intersecting lines
        assert!(do_intersect(&l1, &l2));

        // Non-intersecting lines
        let l3 = (
            Point { x: 5.0, y: 5.0 },
            Point { x: 6.0, y: 6.0 },
        );
        assert!(!do_intersect(&l1, &l3));

        // Collinear but overlapping
        let l4 = (
            Point { x: 2.0, y: 2.0 },
            Point { x: 5.0, y: 5.0 },
        );
        assert!(do_intersect(&l1, &l4));

        // Collinear but non-overlapping
        let l5 = (
            Point { x: 5.0, y: 5.0 },
            Point { x: 7.0, y: 7.0 },
        );
        assert!(!do_intersect(&l1, &l5));

    }

    #[test]
    fn test_find_midpoint() {
        let p1 = Point { x: 0.0, y: 0.0 };
        let p2 = Point { x: 2.0, y: 2.0 };
        let midpoint = find_midpoint(&p1, &p2);
        assert_eq!(midpoint.x, 1.0);
        assert_eq!(midpoint.y, 1.0);
    }

    #[test]
    fn test_find_gradient() {
        let p1 = Point { x: 1.0, y: 1.0 };
        let p2 = Point { x: 4.0, y: 5.0 };
        let gradient = find_gradient(&p1, &p2);
        assert_eq!(gradient, 4.0 / 3.0);

        // Testing vertical line gradient (should panic or handle division by zero gracefully)
        let p3 = Point { x: 2.0, y: 3.0 };
        let p4 = Point { x: 2.0, y: 6.0 };
        let gradient = find_gradient(&p3, &p4);
        assert_eq!(gradient, INFINITY);
    }

    // #[test]
    // fn test_find_points_on_perpendicular_bisector() {
    //     let p1 = Point { x: 0.0, y: 0.0 };
    //     let p2 = Point { x: 2.0, y: 2.0 };
    //     let expected = Ok(
    //         Point ()
    //     )
    //     let (p3, p4) = find_points_on_perpendicular_bisector(&p1, &p2);

    //     // Check that p3 is the midpoint
    //     assert_eq!(p3.x, 1.0);
    //     assert_eq!(p3.y, 1.0);

    //     // Check that p4 lies on the perpendicular bisector
    //     // For this case, the perpendicular bisector passes through (1,1) and is vertical
    //     assert_eq!(p4.x, 0.0);
    //     assert_eq!(p4.y, 2.0);
    // }

    mod test_find_points_on_perpendicular_bisector {
        use super::*;

        #[test]
        fn test_find_points_on_perpendicular_bisector() {
            let p1 = Point { x: 0.0, y: 0.0 };
            let p2 = Point { x: 2.0, y: 2.0 };
            let result = find_points_on_perpendicular_bisector(&p1, &p2);
        
            match result {
                Ok((p3, p4)) => {
                    // Check that p3 is the midpoint
                    assert_eq!(p3.x, 1.0);
                    assert_eq!(p3.y, 1.0);
                
                    // Check that p4 lies on the perpendicular bisector
                    assert_eq!(p4.x, 0.0);
                    assert_eq!(p4.y, 2.0);
                }
                Err(err) => panic!("Unexpected error: {}", err),
            }
        }

        #[test]
        fn test_perpendicular_bisector_horizontal_line() {
            let p1 = Point { x: 0.0, y: 2.0 };
            let p2 = Point { x: 4.0, y: 2.0 };
            let result = find_points_on_perpendicular_bisector(&p1, &p2);
        
            match result {
                Ok((p3, p4)) => {
                    // Midpoint
                    assert_eq!(p3.x, 2.0);
                    assert_eq!(p3.y, 2.0);
                
                    // Perpendicular bisector should be vertical (x = 2.0)
                    assert_eq!(p4.x, 2.0);
                    assert_eq!(p4.y, 0.0);
                }
                Err(err) => panic!("Unexpected error: {}", err),
            }
        }

        #[test]
        fn test_perpendicular_bisector_vertical_line() {
            let p1 = Point { x: 3.0, y: 0.0 };
            let p2 = Point { x: 3.0, y: 4.0 };
            let result = find_points_on_perpendicular_bisector(&p1, &p2);
        
            match result {
                Ok((p3, p4)) => {
                    // Midpoint
                    assert_eq!(p3.x, 3.0);
                    assert_eq!(p3.y, 2.0);
                
                    // Perpendicular bisector should be horizontal (y = 2.0)
                    assert_eq!(p4.x, 0.0);
                    assert_eq!(p4.y, 2.0);
                }
                Err(err) => panic!("Unexpected error: {}", err),
            }
        }

        #[test]
        fn test_perpendicular_bisector_with_diagonal_line() {
            let p1 = Point { x: 0.0, y: 0.0 };
            let p2 = Point { x: 6.0, y: 6.0 };
            let result = find_points_on_perpendicular_bisector(&p1, &p2);
        
            match result {
                Ok((p3, p4)) => {
                    // Midpoint
                    assert_eq!(p3.x, 3.0);
                    assert_eq!(p3.y, 3.0);
                
                    // Check that p4 lies on the perpendicular bisector
                    // Perpendicular bisector: x + y = 6
                    assert!((p4.x + p4.y - 6.0).abs() < 1e-6);
                }
                Err(err) => panic!("Unexpected error: {}", err),
            }
        }

        #[test]
        #[ignore]
        fn test_perpendicular_bisector_negative_coordinates() {
            let p1 = Point { x: -2.0, y: -4.0 };
            let p2 = Point { x: -6.0, y: -8.0 };
            let result = find_points_on_perpendicular_bisector(&p1, &p2);
        
            match result {
                Ok((p3, p4)) => {
                    // Midpoint
                    assert_eq!(p3.x, -4.0);
                    assert_eq!(p3.y, -6.0);
                
                    // Check perpendicular bisector
                    // Slope of line between points = 1. Perpendicular slope = -1
                    // Perpendicular bisector: y = -x - 2
                    assert!((p4.y + p4.x + 2.0).abs() < 1e-6);
                }
                Err(err) => panic!("Unexpected error: {}", err),
            }
        }

        #[test]
        fn test_perpendicular_bisector_identical_points() {
            let p1 = Point { x: 2.0, y: 3.0 };
            let p2 = Point { x: 2.0, y: 3.0 };
        
            let result = find_points_on_perpendicular_bisector(&p1, &p2);
        
            match result {
                Ok(_) => panic!("Expected an error for identical points, but got Ok."),
                Err(err) => assert_eq!(err, "Identical points do not define a line"),
            }
        }


    }

}