use strict;
use warnings;
use oaperlapi;

#Environment
my $scripthome = "C:/code";
my $cmd = "$scripthome/getWeather.bat";

#Get Stats
my $weather = qx{$cmd};
my $temp;
my $humidity;
if ($weather =~ m/temp=(\d+) humidity=(\d+)/) {
	$temp = $1;
	$humidity = $2;
} else {
	$temp = "";
	$humidity = "";
}

# Submit to the OA Perf Data Store via Perl APIs 

my $access = oaperlapi::OAAccess->new();
my $molist = oaperlapi::MetricObservationList->new();
my $interval = time;
my $mo = oaperlapi::MetricObservation->new($interval);

$mo->AddGauge("Weather:Dallas:Temperature","Dallas","Temperature",$temp);
$mo->AddGauge("Weather:Dallas:Humidity","Dallas","Humidity",$humidity);

$molist->AddObservation($mo);
$access->SubmitObservations($molist);
