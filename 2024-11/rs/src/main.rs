use std::thread;
use std::sync::mpsc;
use rand::Rng;
use rs::{has_solution, Point};
use log::{info};
use log::LevelFilter;
use log4rs::append::file::FileAppender;
use log4rs::encode::pattern::PatternEncoder;
use log4rs::config::{Appender, Config, Root};
use chrono::prelude::Utc;

fn main() {
    // setup
   let logfile = FileAppender::builder()
        .encoder(Box::new(PatternEncoder::new("{d} {l} - {m}\n")))
        .build(format!("log/{}.log",Utc::now())).unwrap();

    let config = Config::builder()
        .appender(Appender::builder().build("logfile", Box::new(logfile)))
        .build(Root::builder()
                   .appender("logfile")
                   .build(LevelFilter::Info)).unwrap();

    log4rs::init_config(config).unwrap();

    log::info!("Start");

    // start
    let n: i64 = 100_000_000_000;
    let threads = 10;

    let iterations_per_thread = n / threads;

    let iterations = iterations_per_thread * threads;

    let (tx, rx) = mpsc::channel();

    // Spawn 10 threads.
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
    let results: i64 = rx.iter().take(10).sum();

    info!("Results {}", results);
    info!("Trials {}", iterations);
    let ans = results as f64 / iterations as f64;
    info!("{}", ans);
    println!("{}", ans);


}

fn task(n: &i64) -> i64 {
    let mut rng = rand::thread_rng();

    let mut results = 0; 
    for _ in 1..*n {
        let red = Point {
            x: rng.gen::<f64>(),
            y: rng.gen::<f64>()
        };

        let blue = Point {
            x: rng.gen::<f64>(),
            y: rng.gen::<f64>()
        };

        match has_solution(&blue, &red) {
            Ok(true) => {
                results = results + 1;
            },
            Ok(false) => (),
            Err(_e) => eprintln!("something happened {}", _e)
        }
    }

    results

}
