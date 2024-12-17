use chrono::prelude::Utc;
use log::LevelFilter;
use log::{debug, info, trace};
use log4rs::append::file::FileAppender;
use log4rs::config::{Appender, Config, Root};
use log4rs::encode::pattern::PatternEncoder;
use rand::Rng;
use rs::{has_solution, Point};
use std::env;
use std::sync::mpsc;
use std::thread;

fn main() {
    // setup
    let logfile = FileAppender::builder()
        .encoder(Box::new(PatternEncoder::new("{d} {l} - {m}\n")))
        .build(format!("log/{}.log", Utc::now()))
        .unwrap();

    let config = Config::builder()
        .appender(Appender::builder().build("logfile", Box::new(logfile)))
        .build(Root::builder().appender("logfile").build(LevelFilter::Info))
        .unwrap();

    log4rs::init_config(config).unwrap();

    log::info!("Start");

    let args: Vec<String> = env::args().collect();
    debug!("{:?}", args);

    // start
    let n: u64 = match args[1].parse::<u32>() {
        Ok(n) => 10_u64.pow(n),
        Err(_e) => {
            eprintln!("Error {}", _e);
            panic!("Invalid input for n provided")
        }
    };

    let threads = 10;

    let iterations_per_thread = n / threads;

    let iterations = iterations_per_thread * threads;

    let (tx, rx) = mpsc::channel();

    // Spawn threads.
    let mut handles = Vec::new();
    for _ in 0..threads {
        let tx = tx.clone();
        let handle = thread::spawn(move || {
            let result = task(&iterations_per_thread);
            tx.send(result).expect("Failed to send result");
        });
        handles.push(handle);
    }

    // Wait for all threads to complete.
    for handle in handles {
        handle.join().expect("Thread panicked");
    }

    // Collect the results and calculate the sum.
    let results: u64 = rx.iter().take(threads as usize).sum();

    info!("Results {}", results);
    info!("Trials {}", iterations);
    let ans = results as f64 / iterations as f64;
    info!("{}", ans);
    println!("{}", ans);
}

fn task(n: &u64) -> u64 {
    let mut rng = rand::thread_rng();

    let mut results = 0;
    for _ in 1..*n {
        let red = Point {
            x: rng.gen_range(0.0..1.0),
            y: rng.gen_range(0.0..1.0),
        };

        let blue = Point {
            x: rng.gen_range(0.0..1.0),
            y: rng.gen_range(0.0..1.0),
        };

        trace!("{:?} {:?}", blue, red);

        match has_solution(&blue, &red) {
            Ok(true) => {
                results += 1;
                trace!("Solution found")
            }
            Ok(false) => (),
            Err(_e) => eprintln!("something happened {}", _e),
        }
    }

    results
}
