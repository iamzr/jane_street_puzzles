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

enum Edges {
    Top,
    Bottom,
    Left,
    Right
}

fn get_closest_side(p: &Point) -> Result<Edges, &'static str> {
    let x = p.x;
    let y = p.y;

    if y <= x && y < 1.0 - x {
        Ok(Edges::Bottom)
    } else if y > x && y <= 1.0 - x {
        Ok(Edges::Left)
    } else if y >= x && y > 1.0 - x {
        Ok(Edges::Top)
    } else if y < x && y >= 1.0 - x {
        Ok(Edges::Right)
    } else if x == 0.5 && y == 0.5 {
        Ok(Edges::Bottom)
    } else {
        Err("Something's gone wrong")
    }
}


pub fn has_solution(blue: &Point, red: &Point) -> Result<bool, &'static str> {
    let edge = match  get_closest_side(blue) {
        Ok(edge) => edge,
        Err(_e) => {
            eprintln!("something went wrong {}", _e);
            return Err(_e);
        }
    };

    if blue == red {
        return Err("Identical points do not define a line")
    }

    let m = find_midpoint(blue, red);
    let g = -(1.0 / find_gradient(red, blue));

    let c = ( g* -m.x) + m.y;

    let check = match edge {
        Edges::Bottom => -c / g,
        Edges::Left=> c,
        Edges::Top=> (1.0-c) / g,
        Edges::Right => g + c,
    };

    Ok(check <= 1.0 && check >= 0.0)



}

#[cfg(test)]
mod tests {
    use super::*;
    mod test_has_solution {
        use super::*;

        #[test]
        fn test_identical_points() {
            let blue = Point { x: 0.0, y: 0.0 };
            let red = Point { x: 0.0, y: 0.0 };

            // Expect an error because the points are identical
            let result = has_solution(&blue, &red);
            assert_eq!(result, Err("Identical points do not define a line"));
        }

        #[test]
        fn test_solution_doesnt_exists_bottom_edge() {
            let blue = Point { x: 0.5, y: 0.2 };
            let red = Point { x: 0.5, y: 0.8 };

            // Mocking or ensuring the edge returned is `edges::bottom`
            let result = has_solution(&blue, &red);
            assert_eq!(result, Ok(false));  // Adjust based on the actual logic
        }

        #[test]
        fn test_solution_exists_top_edge() {
            let blue = Point { x: 0.41903142181567776, y: 0.6453315775286078 };
            let red = Point { x: 0.7049400139371284, y: 0.8198186859873597 };

            let result = has_solution(&blue, &red);
            assert_eq!(result, Ok(true)); 
            }

        #[test]
        fn test_another_one() {
            let blue = Point { x: 0.24847643665677582, y: 0.2975835100602469 };
            let red = Point { x: 0.11274437235696835, y: 0.7160251321672993 };


            let result = has_solution(&blue, &red);
            assert_eq!(result, Ok(true));

        }


    }

    mod test_find_midpoint {
        use super::*;

        #[test]
        fn test_find_midpoint() {
            let p1 = Point { x: 0.0, y: 0.0 };
            let p2 = Point { x: 2.0, y: 2.0 };
            let midpoint = find_midpoint(&p1, &p2);
            assert_eq!(midpoint.x, 1.0);
            assert_eq!(midpoint.y, 1.0);
        }

    }

    mod test_find_gradient {
        use super::*;
        use std::f64::INFINITY;

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

    }
}
