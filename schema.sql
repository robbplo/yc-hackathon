create table users (
  id bigint generated always as identity primary key,
  first_name text not null,
  last_name text not null,
  phone text unique not null,
  date_registered timestamp default now()
);

create table mollie_customers (
  id bigint generated always as identity primary key,
  user_id bigint references users(id) on delete cascade,
  mollie_customer_id text not null,
  created_at timestamp default now()
);

create table subscriptions (
  id bigint generated always as identity primary key,
  user_id bigint references users(id) on delete cascade,
  mollie_subscription_id text not null,
  plan text,
  subscription_start timestamp default now(),
  subscription_end timestamp,
  status text default 'active'
);
